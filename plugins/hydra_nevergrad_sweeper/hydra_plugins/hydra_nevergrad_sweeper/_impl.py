# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
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
from hydra.core.config_loader import ConfigLoader
from hydra.core.override_parser.hpo import (
    HPOParameter,
    create_hpo_parameter_from_override,
)
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.override_parser.types import Override
from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.plugins.sweeper import Sweeper
from hydra.types import TaskFunction
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


def create_nevergrad_parameter_from_hpo_parameter(hpo_parameter: HPOParameter) -> Any:
    if hpo_parameter.type == "fixed":
        return hpo_parameter.values[0]
    elif hpo_parameter.type == "choice":
        if "ordered" in hpo_parameter.tags:
            return ng.p.TransitionChoice(hpo_parameter.values)
        else:
            return ng.p.Choice(hpo_parameter.values)
    elif hpo_parameter.type == "range":
        return ng.p.Choice(hpo_parameter.values)
    elif hpo_parameter.type == "interval":
        lower = hpo_parameter.values[0]
        upper = hpo_parameter.values[1]
        if hpo_parameter.log:
            scalar = ng.p.Log(lower=lower, upper=upper)
        else:
            scalar = ng.p.Scalar(lower=lower, upper=upper)  # type: ignore
        if isinstance(lower, int):
            scalar.set_integer_casting()
        return scalar


def create_nevergrad_parameter_from_override(override: Override) -> Any:
    hpo_param = create_hpo_parameter_from_override(override=override)
    return hpo_param.name, create_nevergrad_parameter_from_hpo_parameter(hpo_param)


class NevergradSweeperImpl(Sweeper):
    def __init__(
        self,
        optim: OptimConf,
        parametrization: Optional[DictConfig],
    ):
        self.opt_config = optim
        self.config: Optional[DictConfig] = None
        self.launcher: Optional[Launcher] = None
        self.job_results = None
        self.parametrization: Dict[str, Any] = {}
        if parametrization is not None:
            assert isinstance(parametrization, DictConfig)
            self.parametrization = {
                x: create_nevergrad_param_from_config(y)
                for x, y in parametrization.items()
            }
        self.job_idx: Optional[int] = None

    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        self.job_idx = 0
        self.config = config
        self.config_loader = config_loader
        self.launcher = Plugins.instance().instantiate_launcher(
            config=config, config_loader=config_loader, task_function=task_function
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
            name, nevergrad_param = create_nevergrad_parameter_from_override(override)
            params[name] = nevergrad_param
        parametrization = ng.p.Dict(**params)
        parametrization.descriptors.deterministic_function = not self.opt_config.noisy
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
            self.job_idx += len(returns)
            # would have been nice to avoid waiting for all jobs to finish
            # aka batch size Vs steady state (launching a new job whenever one is done)
            for cand, ret in zip(candidates, returns):
                loss = direction * ret.return_value
                optimizer.tell(cand, loss)
                if loss < best[0]:
                    best = (loss, cand)
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
