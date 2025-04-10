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
    Callable,
)

import numpy as np
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
from omegaconf import DictConfig, OmegaConf

from .config import OptimConf, ScalarOrArrayConfigSpec, CheapConstraintFn

log = logging.getLogger(__name__)


def create_nevergrad_param_from_config(
    config: Union[MutableSequence[Any], MutableMapping[str, Any]]
) -> Any:
    if OmegaConf.is_config(config):
        config = OmegaConf.to_container(config, resolve=True)
    if isinstance(config, MutableSequence):
        return ng.p.Choice(config)
    if isinstance(config, MutableMapping):
        specs = ScalarOrArrayConfigSpec(**config)
        init = ["init", "lower", "upper"]
        init_params = {x: getattr(specs, x) for x in init}

        if specs.shape or isinstance(init_params["init"], list):
            if specs.shape:
                init_params["shape"] = specs.shape
            parameter = ng.p.Array(**init_params)
            if specs.step is not None:
                parameter.set_mutation(sigma=specs.step)
        elif not specs.log:
            parameter = ng.p.Scalar(**init_params)
            if specs.step is not None:
                parameter.set_mutation(sigma=specs.step)
        else:
            if specs.step is not None:
                init_params["exponent"] = specs.step
            parameter = ng.p.Log(**init_params)
        if specs.integer:
            parameter.set_integer_casting()
        return parameter


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
        parameterization: Optional[DictConfig],
    ):
        self.opt_config = optim
        self.config: Optional[DictConfig] = None
        self.launcher: Optional[Launcher] = None
        self.hydra_context: Optional[HydraContext] = None
        self.job_results = None
        self.parameterization: Dict[str, Any] = {}
        if parameterization is not None:
            assert isinstance(parameterization, DictConfig)
            self.parameterization = {
                str(x): create_nevergrad_param_from_config(y)
                for x, y in parameterization.items()
            }
        self.cheap_constraints: List[CheapConstraintFn] = []
        if optim.cheap_constraints is not None:
            for constraint in optim.cheap_constraints.values():
                self.cheap_constraints.append(constraint)
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
        # Override the parameterization from commandline
        params = dict(self.parameterization)

        parser = OverridesParser.create()
        parsed = parser.parse_overrides(arguments)

        for override in parsed:
            params[override.get_key_element()] = (
                create_nevergrad_parameter_from_override(override)
            )

        parameterization = ng.p.Dict(**params)
        parameterization.function.deterministic = not self.opt_config.noisy
        parameterization.random_state.seed(self.opt_config.seed)
        for constraint in self.cheap_constraints:
            parameterization.register_cheap_constraint(constraint)
        # log and build the optimizer
        opt = self.opt_config.optimizer
        remaining_budget = self.opt_config.budget
        nw = self.opt_config.num_workers
        log.info(
            f"NevergradSweeper(optimizer={opt}, budget={remaining_budget}, "
            f"num_workers={nw}) {name}"
        )
        log.info(f"with parameterization {parameterization}")
        log.info(f"Sweep output dir: {self.config.hydra.sweep.dir}")
        if self.opt_config.load_if_exists is not None and self.opt_config.load_if_exists.exists():
            optimizer = ng.optimizers.registry[opt].load(self.opt_config.load_if_exists)
            log.info(f"Resuming nevergrad optimization from budget={optimizer.num_ask} or {remaining_budget}")
            remaining_budget -= optimizer.num_ask
            self.job_idx = optimizer.num_ask
        else:
            log.info(f"Initializing optimizer from scratch with budget={remaining_budget}")
            optimizer = ng.optimizers.registry[opt](parameterization, remaining_budget, nw)
        for callback_spec in self.opt_config.callbacks.values():
            optimizer.register_callback(callback_spec.name, callback_spec.callback)
        # loop!
        all_returns: List[Any] = []
        best: Tuple[float, ng.p.Parameter] = (float("inf"), parameterization)
        while remaining_budget > 0:
            batch = min(nw, remaining_budget)
            remaining_budget -= batch
            candidates = [optimizer.ask() for _ in range(batch)]
            overrides = list(
                tuple(
                    f"{x}={y.tolist() if isinstance(y, np.ndarray) else y}"
                    for x, y in c.value.items()
                )
                for c in candidates
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
            "best_evaluated_params": {
                k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in best[1].value.items()
            },
            "best_evaluated_result": direction * best[0],
        }
        OmegaConf.save(
            OmegaConf.create(results_to_serialize),
            f"{self.config.hydra.sweep.dir}/optimization_results.yaml",
        )
        log.info(
            "Best parameters: %s", " ".join(f"{x}={y}" for x, y in recom.value.items())
        )
