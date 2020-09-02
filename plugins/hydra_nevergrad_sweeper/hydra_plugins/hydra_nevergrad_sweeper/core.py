# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from typing import Any, Dict, List, Optional, Tuple

import nevergrad as ng
from hydra.core.config_loader import ConfigLoader
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.override_parser.types import Override
from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.plugins.sweeper import Sweeper
from hydra.types import TaskFunction
from omegaconf import DictConfig, ListConfig, OmegaConf

from .config import OptimConf, ScalarConfigSpec

# pylint: disable=logging-fstring-interpolation,no-self-used
log = logging.getLogger(__name__)


def get_nevergrad_parameter(description: Any) -> Any:
    """
     Maps Hydra override to nevergrad params
     # regardless of the choice values, choice is always unordered p.Choice:
     choice(a,b,c)  =>  ng.p.Choice(["a", "b", "c"])

     # We can support forcing a choice to be ordered by tagging it:
     # (I prefer order over transition(al). at least to me it's clearer.
     tag(ordered, choice(a,b,c)) ==> ng.p.TransitionChoice(["a","b","c"])

     # ranges are always ordered:
     range(1,12)  =>  ng.p.Scalar(lower=1, upper=12, step=1)

     # intervals are scalars:
     # Note: by intervals are always interpreted as floats (even for int start and end values).
     interval(0,1)     -> RangeSweep(start=0.0, end=1.0) -> ng.p.Scalar(lower=0.0, upper=1.0)
     interval(0.0,1.0) -> RangeSweep(start=0.0, end=1.0) -> ng.p.Scalar(lower=0.0, upper=1.0)

     # a user can cast the interval to int to override that:
     int(interval(0,1) -> RangeSweep(start=0, end=1) -> ng.p.Scalar(lower=0.0, upper=1.0).set_integer_casting()
     """
    scalar = None
    if isinstance(description, Override):
        override = description
        val = override.value()
        if override.is_sweep_override():
            if override.is_choice_sweep():
                if "ordered" in val.tags:
                    return ng.p.TransitionChoice(val.list)
                else:
                    return ng.p.Choice(val.list)
            elif override.is_range_sweep():
                params = {"lower": val.start, "upper": val.stop}
                scalar = ng.p.Scalar(**params)
                scalar.set_mutation(sigma=val.step)
                scalar.integer = isinstance(val.start, int)
            elif override.is_interval_sweep():  # continuous variable
                if "log" in val.tags:
                    scalar = ng.p.Log(lower=val.start, upper=val.end)
                else:
                    scalar = ng.p.Scalar(lower=val.start, upper=val.end)
                if isinstance(val.start, int):
                    scalar.set_integer_casting()
        else:
            return val
    if isinstance(description, (list, ListConfig)):
        return ng.p.Choice(list(description))
    if isinstance(description, (dict, DictConfig)):
        description = ScalarConfigSpec(**description)
        init = ["init", "lower", "upper"]
        init_params = {x: getattr(description, x) for x in init}
        if not description.log:
            scalar = ng.p.Scalar(**init_params)
            if description.step is not None:
                scalar.set_mutation(sigma=description.step)
        else:
            if description.step is not None:
                init_params["exponent"] = description.step
            scalar = ng.p.Log(**init_params)
        if description.integer:
            scalar.set_integer_casting()

    if scalar:
        if scalar.integer:
            a, b = scalar.bounds
            if a is not None and b is not None and b - a <= 6:
                raise ValueError(
                    "For integers with 6 or fewer values, use a choice instead"
                )
        return scalar

    raise ValueError(f"Cannot parse description: {description}.")


class CoreNevergradSweeper(Sweeper):
    """Returns a Nevergrad parameter from a definition string.

    Parameters
    ----------
    config: DictConfig
      the optimization process configuration
    version: int
      version of the API
    """

    def __init__(
        self, optim: OptimConf, version: int, parametrization: Optional[DictConfig]
    ):
        assert (
            version == 1
        ), f"Only version 1 of API is currently available (got {version})"
        self.opt_config = optim
        self.config: Optional[DictConfig] = None
        self.launcher: Optional[Launcher] = None
        self.job_results = None
        self.parametrization: Dict[str, Any] = {}
        if parametrization is not None:
            assert isinstance(parametrization, DictConfig)
            self.parametrization = {
                x: get_nevergrad_parameter(y) for x, y in parametrization.items()
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
            params[override.get_key_element()] = get_nevergrad_parameter(override)

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
