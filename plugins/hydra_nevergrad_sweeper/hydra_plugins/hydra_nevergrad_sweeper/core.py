# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import itertools
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from omegaconf import DictConfig, ListConfig, OmegaConf

from hydra.core.config_loader import ConfigLoader
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.plugins.search_path_plugin import SearchPathPlugin
from hydra.plugins.sweeper import Sweeper
from hydra.types import TaskFunction

# pylint: disable=logging-fstring-interpolation,no-self-used

log = logging.getLogger(__name__)


class NevergradSearchPathPlugin(SearchPathPlugin):
    def manipulate_search_path(self, search_path: ConfigSearchPath) -> None:
        search_path.append(
            "nevergrad", "pkg://hydra_plugins.hydra_nevergrad_sweeper.conf"
        )


@dataclass
class CommandlineSpec:
    bounds: Optional[Tuple[float, float]] = None
    options: Optional[List[str]] = None
    cast: str = "float"
    log: bool = False

    def __post_init__(self) -> None:
        if not (self.bounds is None) ^ (self.options is None):
            raise ValueError("Exactly one of bounds or options must be specified")
        if self.bounds is not None:
            if self.cast == "str":
                raise ValueError(
                    "Inconsistent specifications 'str' for bounded values."
                )
            if self.bounds[0] > self.bounds[1]:
                raise ValueError(f"Bounds must be ordered, but got {self.bounds}")
        if self.options is not None and self.log:
            raise ValueError("Inconsistent 'log' specification for choice parameter")

    @classmethod
    def parse(cls, string: str) -> "CommandlineSpec":
        available_modifiers = {"log", "float", "int", "str"}
        colon_split = string.split(":")
        modifiers = set(
            itertools.takewhile(available_modifiers.__contains__, colon_split)
        )
        remain = colon_split[len(modifiers) :]
        casts = list(modifiers - {"log"})
        if len(remain) not in {1, 2}:
            raise ValueError(
                "Can't interpret non-speficiations: {}.\nthis needs to be "
                "either colon or coma-separated values".format(":".join(remain))
            )
        if len(casts) > 1:
            raise ValueError(f"Inconsistent specifications: {casts}")
        if len(remain) == 1:  # choice argument
            cast = casts[0] if casts else "str"
            options = remain[0].split(",")
            if len(options) < 2:
                raise ValueError("At least 2 options are required")
            if not casts:
                try:  # default to float if possible and no spec provided
                    _ = [float(x) for x in options]
                    cast = "float"
                except ValueError:
                    pass
            return cls(options=options, cast=cast)
        # bounded argument
        bounds: Tuple[float, float] = tuple(float(x) for x in remain)  # type: ignore
        cast = casts[0] if casts else "float"
        return cls(bounds=bounds, cast=cast, log="log" in modifiers)


def make_nevergrad_parameter(description: Any) -> Any:
    """Returns a Nevergrad parameter from a definition string or object.

    Parameters
    ----------
    description: Any
       - a definition string. This can be:
         - comma-separated values: for a choice parameter
           Eg.: "a,b,c"
           Note: sequences of increasing scalars provide a specific parametrization
             compared to unordered categorical values
         - ":"-separated values for ranges of scalars.
           "int" and/or "log" modifiers can be added in front to cast to integer or
           use log-distributed values (Eg: int:log:4:1024)
         - evaluable nevergrad Parameter definition, which will be evaluated at
           runtime. This provides full nevergrad flexibility at the cost of robustness.
           Eg.:"Log(a_min=0.001, a_max=0.1)"
         - anything else will be treated as a constant string
       - a definition dict for scalar parameters, with potential fields
         init, lower, upper, step, log, integer
       - a list for option parameters

    Returns
    -------
    Parameter or str
        A Parameter if the string fitted one of the definitions, else the input string
    """
    # lazy initialization to avoid overhead when loading hydra
    import nevergrad as ng

    # revert config parsing

    if isinstance(description, (ListConfig, list)):
        description = ",".join(description)
    if isinstance(description, str):
        # hacky nevergrad parameter
        if description.startswith(tuple(dir(ng.p))):
            param: ng.p.Parameter = eval(
                "ng.p." + description
            )  # pylint: disable=eval-used
            assert isinstance(param, ng.p.Parameter)
            return param
        # cast to spec if possible
        try:
            description = CommandlineSpec.parse(description)
        except ValueError:
            pass
    # convert scalar specs to dict
    if isinstance(description, CommandlineSpec) and description.bounds is not None:
        description = dict(
            lower=description.bounds[0],
            upper=description.bounds[1],
            log=description.log,
            integer=description.cast == "int",
        )
    # convert dict to Scalar parameter instance
    if isinstance(description, (dict, DictConfig)):
        init = ["init", "lower", "upper"]
        options = init + ["log", "step", "integer"]
        assert all(x in options for x in description)
        init_params = {x: y for x, y in description.items() if x in init}
        if not description.get("log", False):
            scalar = ng.p.Scalar(**init_params)
            if "step" in description:
                scalar.set_mutation(sigma=description["step"])
        else:
            if "step" in description:
                init_params["exponent"] = description["step"]
            scalar = ng.p.Log(**init_params)
        if description.get("integer", False):
            scalar.set_integer_casting()
            a, b = scalar.bounds
            if a is not None and b is not None and b - a <= 6:
                raise ValueError(
                    "For integers with 6 or fewer values, use a choice instead"
                )
        return scalar
    # choices
    if isinstance(description, CommandlineSpec):
        assert description.options is not None
        caster = {"int": int, "str": str, "float": float}[description.cast]
        choices = [caster(x) for x in description.options]
        ordered = all(isinstance(c, (int, float)) for c in choices)
        ordered &= all(
            c0 <= c1 for c0, c1 in zip(choices[:-1], choices[1:])  # type: ignore
        )
        return ng.p.TransitionChoice(choices) if ordered else ng.p.Choice(choices)
    # constant
    if isinstance(description, (str, int, float)):
        return description
    raise TypeError(f"Unexpected parameter configuration: {description}")


class NevergradSweeper(Sweeper):
    """Returns a Nevergrad parameter from a definition string.

    Parameters
    ----------
    config: DictConfig
      the optimization process configuration
    version: int
      version of the API
    """

    def __init__(
        self, optim: DictConfig, version: int, parametrization: Optional[DictConfig],
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
                x: make_nevergrad_parameter(y) for x, y in parametrization.items()
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
        self.launcher = Plugins.instance().instantiate_launcher(
            config=config, config_loader=config_loader, task_function=task_function
        )

    def sweep(self, arguments: List[str]) -> None:
        # lazy initialization to avoid overhead when loading hydra
        import nevergrad as ng

        assert self.config is not None
        assert self.launcher is not None
        assert self.job_idx is not None
        direction = -1 if self.opt_config.maximize else 1
        name = "maximization" if self.opt_config.maximize else "minimization"
        # Override the parametrization from commandline
        params = dict(self.parametrization)
        for s in arguments:
            key, value = s.split("=", 1)
            params[key] = make_nevergrad_parameter(value)
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
