# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import math
from typing import (
    Any,
    Dict,
    List,
    MutableMapping,
    MutableSequence,
    Optional,
    Tuple,
    Union,
)

import nevergrad as ng
from hydra.core import utils
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.override_parser.types import (
    ChoiceSweep,
    IntervalSweep,
    Override,
    Transformer,
)
from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.plugins.sweeper import Sweeper
from hydra.types import HydraContext, TaskFunction
from omegaconf import DictConfig, ListConfig, OmegaConf

from .config import OptimConf, ScalarConfigSpec

log = logging.getLogger(__name__)


def create_nevergrad_param_from_config(
    config: Union[MutableSequence[Any], MutableMapping[str, Any]]
) -> Any:
    if isinstance(config, MutableSequence):
        if isinstance(config, ListConfig):
            config = OmegaConf.to_container(config, resolve=True)  # type: ignore
        return ng.p.Choice(config)
    if isinstance(config, MutableMapping):
        specs = ScalarConfigSpec(**config)
        init = ["init", "lower", "upper"]
        init_params = {x: getattr(specs, x) for x in init}
        if not specs.log:
            scalar = ng.p.Scalar(**init_params)
            if specs.step is not None:
                scalar.set_mutation(sigma=specs.step)
        else:
            if specs.step is not None:
                init_params["exponent"] = specs.step
            scalar = ng.p.Log(**init_params)
        if specs.integer:
            scalar.set_integer_casting()
        return scalar
    return config


def create_nevergrad_parameter_from_override(override: Override) -> Any:
    val = override.value()
    if not override.is_sweep_override():
        return override.get_value_element_as_str()
    if override.is_choice_sweep():
        assert isinstance(val, ChoiceSweep)
        vals = [x for x in override.sweep_iterator(transformer=Transformer.encode)]
        if "ordered" in val.tags:
            return ng.p.TransitionChoice(vals)
        else:
            return ng.p.Choice(vals)
    elif override.is_range_sweep():
        vals = [x for x in override.sweep_iterator(transformer=Transformer.encode)]
        return ng.p.Choice(vals)
    elif override.is_interval_sweep():
        assert isinstance(val, IntervalSweep)
        if "log" in val.tags:
            scalar = ng.p.Log(lower=val.start, upper=val.end)
        else:
            scalar = ng.p.Scalar(lower=val.start, upper=val.end)
        if isinstance(val.start, int):
            scalar.set_integer_casting()
        return scalar


class NevergradSweeperImpl(Sweeper):
    def __init__(
        self,
        optim: OptimConf,
        parametrization: Optional[DictConfig],
    ):
        self.opt_config = optim
        self.config: Optional[DictConfig] = None
        self.launcher: Optional[Launcher] = None
        self.hydra_context: Optional[HydraContext] = None
        self.job_results = None
        self.parametrization: Dict[str, Any] = {}
        if parametrization is not None:
            assert isinstance(parametrization, DictConfig)
            self.parametrization = {
                str(x): create_nevergrad_param_from_config(y)
                for x, y in parametrization.items()
            }
        self.job_idx: Optional[int] = None

    def setup(
        self,
        *,
        hydra_context: HydraContext,
        task_function: TaskFunction,
        config: DictConfig,
    ) -> None:
        self.job_idx = 0
        self.config = config
        self.hydra_context = hydra_context
        self.launcher = Plugins.instance().instantiate_launcher(
            hydra_context=hydra_context, task_function=task_function, config=config
        )

    def sweep(self, arguments: List[str]) -> None:
        assert self.config is not None
        assert self.launcher is not None
        assert self.job_idx is not None
        direction = -1 if self.opt_config.maximize else 1
        name = "maximization" if self.opt_config.maximize else "minimization"
        # Override the parametrization from commandline
        params = dict(self.parametrization)

        parser = OverridesParser.create()
        parsed = parser.parse_overrides(arguments)

        for override in parsed:
            params[override.get_key_element()] = (
                create_nevergrad_parameter_from_override(override)
            )

        parametrization = ng.p.Dict(**params)
        parametrization.function.deterministic = not self.opt_config.noisy
        parametrization.random_state.seed(self.opt_config.seed)
        # log and build the optimizer
        opt = self.opt_config.optimizer
        remaining_budget = self.opt_config.budget
        nw = self.opt_config.num_workers
        log.info(
            f"NevergradSweeper(optimizer={opt}, budget={remaining_budget}, "
            f"num_workers={nw}) {name}"
        )
        log.info(f"with parametrization {parametrization}")
        log.info(f"Sweep output dir: {self.config.hydra.sweep.dir}")
        optimizer = ng.optimizers.registry[opt](parametrization, remaining_budget, nw)
        # loop!
        all_returns: List[Any] = []
        best: Tuple[float, ng.p.Parameter] = (float("inf"), parametrization)
        while remaining_budget > 0:
            batch = min(nw, remaining_budget)
            remaining_budget -= batch
            candidates = [optimizer.ask() for _ in range(batch)]
            overrides = list(
                tuple(f"{x}={y}" for x, y in c.value.items()) for c in candidates
            )
            self.validate_batch_is_legal(overrides)
            returns = self.launcher.launch(overrides, initial_job_idx=self.job_idx)
            # would have been nice to avoid waiting for all jobs to finish
            # aka batch size Vs steady state (launching a new job whenever one is done)
            self.job_idx += len(returns)
            # check job status and prepare losses
            failures = 0
            for cand, ret in zip(candidates, returns):
                if ret.status == utils.JobStatus.COMPLETED:
                    rectified_loss = direction * ret.return_value
                else:
                    rectified_loss = math.inf
                    failures += 1
                    try:
                        ret.return_value
                    except Exception as e:
                        log.warning(f"Returning infinity for failed experiment: {e}")
                optimizer.tell(cand, rectified_loss)
                if rectified_loss < best[0]:
                    best = (rectified_loss, cand)
            # raise if too many failures
            if failures / len(returns) > self.opt_config.max_failure_rate:
                log.error(
                    f"Failed {failures} times out of {len(returns)} "
                    f"with max_failure_rate={self.opt_config.max_failure_rate}"
                )
                for ret in returns:
                    ret.return_value  # delegate raising to JobReturn, with actual traceback
            all_returns.extend(returns)
        recom = optimizer.provide_recommendation()
        results_to_serialize = {
            "name": "nevergrad",
            "best_evaluated_params": best[1].value,
            "best_evaluated_result": direction * best[0],
        }
        OmegaConf.save(
            OmegaConf.create(results_to_serialize),
            f"{self.config.hydra.sweep.dir}/optimization_results.yaml",
        )
        log.info(
            "Best parameters: %s", " ".join(f"{x}={y}" for x, y in recom.value.items())
        )
