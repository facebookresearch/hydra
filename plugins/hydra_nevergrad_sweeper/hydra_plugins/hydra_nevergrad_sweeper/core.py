# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import json
import logging
from typing import Any, Dict, List, Optional, Union

import nevergrad as ng  # type: ignore
from omegaconf import DictConfig, OmegaConf

from hydra.core.config_loader import ConfigLoader
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.plugins.search_path_plugin import SearchPathPlugin
from hydra.plugins.sweeper import Sweeper
from hydra.types import TaskFunction

log = logging.getLogger(__name__)


class NevergradSearchPathPlugin(SearchPathPlugin):
    """
    This plugin is allowing configuration files provided by this sweeper plugin to be discovered
    and used once it is installed.
    """

    def manipulate_search_path(self, search_path: ConfigSearchPath) -> None:
        # Appends the search path for this plugin to the end of the search path
        search_path.append(
            "nevergrad-sweeper", "pkg://hydra_plugins.hydra_nevergrad_sweeper.conf"
        )


def convert_to_deduced_type(string: str) -> Union[int, float, str]:
    """Converts a string into a float or an int if it makes sense,
    or returns the string.

    Examples
    --------
    read_value("1")
    >>> 1

    read_value("1.0")
    >>> 1.0

    read_value("blublu")
    >>> "blublu"
    """
    output: Union[float, int, str] = string
    try:
        output = float(string)
    except ValueError:
        pass
    else:
        if output.is_integer() and "." not in string:
            output = int(output)
    return output


def make_parameter(string: str) -> Union[int, float, str, ng.p.Parameter]:
    """Returns a Nevergrad parameter from a definition string.

    Parameters
    ----------
    string: str
         a definition string. This can be:
         - comma-separated values: for a choice parameter
           Eg.: "a,b,c"
           Note: sequences of increasing scalars provide a specific parametrization
             compared to unordered categorical values
         - ":"-separated values for ranges of scalars.
           Eg.: "1.0:5.0"
           Note: using integers as bounds will parametrize as an integer value
         - evaluable nevergrad Parameter definition, which will be evaluated at
           runtime. This provides full nevergrad flexibility at the cost of robustness.
           Eg.:"Log(a_min=0.001, a_max=0.1)"
         - anything else will be treated as a constant string

    Returns
    -------
    Parameter or str
        A Parameter if the string fitted one of the definitions, else the input string
    """
    string = string.strip()
    if string.startswith(tuple(dir(ng.p))):
        param = eval("ng.p." + string)  # pylint: disable=eval-used
        assert isinstance(param, ng.p.Parameter)
        return param
    if "," in string:
        choices = [convert_to_deduced_type(x) for x in string.split(",")]
        ordered = all(isinstance(c, (int, float)) for c in choices)
        ordered &= all(
            c0 <= c1 for c0, c1 in zip(choices[:-1], choices[1:])  # type: ignore
        )
        return ng.p.TransitionChoice(choices) if ordered else ng.p.Choice(choices)
    if ":" in string:
        a, b = [convert_to_deduced_type(x) for x in string.split(":")]
        assert all(
            isinstance(c, (int, float)) for c in (a, b)
        ), "Bounds must be scalars"
        sigma = (b - a) / 6  # type: ignore
        scalar = (
            ng.p.Scalar(init=(a + b) / 2.0)  # type: ignore
            .set_mutation(sigma=sigma)
            .set_bounds(a_min=a, a_max=b, full_range_sampling=True)
        )
        if all(isinstance(c, int) for c in (a, b)):
            scalar.set_integer_casting()
        return scalar
    return convert_to_deduced_type(string)  # constant


class NevergradSweeper(Sweeper):
    """Returns a Nevergrad parameter from a definition string.

    Parameters
    ----------
    optimizer: str
       name of a Nevergrad optimizer to use. Some interesting options are:
         - "OnePlusOne" extemely simple and robust, especially at low budget, but
           tends to converge early.
         - "CMA" very good algorithm, but may require a significant budget (> 120)
         - "TwoPointsDE": an algorithm good in a wide range of settings, for significant budgets
           (> 120).
         - "Shiva" an algorithm aiming at identifying the best optimizer given your input
           definition (work in progress, it may still be ill-suited for low budget)
       See nevergrad documentation: https://facebookresearch.github.io/nevergrad/
    budget: int
       the total number of function evaluation that can be performed
    num_workers: int
       the number of evaluation to run in parallel. Sequential means num_workers=1.
       Population based algorithms such as CMA and DE can have num_workers up to 40 without slowing
       down the convergence, while OnePlusOne can benefit sequential, but will perform well with several
       workers as well.
    noisy: bool
       notifies (some) algorithms that the function evaluation is noisy
    maximize: bool
       whether to perform maximization instead of default minimization
    seed: int
        seed for the optimizer for reproducibility. If the seed is -1, the optimizer is not seeded (default)
    version: int
       the version of the commandline input parsing. The parsing will probably evolve in the near
       future and several versions may temporarily coexist.
       s
    """

    def __init__(
        self,
        optimizer: str,
        budget: int,
        num_workers: int,
        noisy: bool,
        maximize: bool,
        seed: Optional[int],
        version: int,
    ):
        self.config: Optional[DictConfig] = None
        self.launcher: Optional[Launcher] = None
        assert version == 1, "Only version 1 of API is currently available"
        self.job_results = None
        self.optimizer = optimizer
        self.noisy = noisy
        self.budget = budget
        self.num_workers = num_workers
        self.seed = seed
        self._direction = -1 if maximize else 1

    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        self.config = config
        self.launcher = Plugins.instantiate_launcher(
            config=config, config_loader=config_loader, task_function=task_function
        )

    def sweep(self, arguments: List[str]) -> None:
        assert self.config is not None
        assert self.launcher is not None
        # Construct the parametrization
        params: Dict[str, Union[str, int, float, ng.p.Parameter]] = {}
        for s in arguments:
            key, value = s.split("=", 1)
            params[key] = make_parameter(value)
        parametrization = ng.p.Dict(**params)
        parametrization.descriptors.deterministic_function = not self.noisy
        parametrization.random_state.seed(self.seed)
        # log and build the optimizer
        name = "maximization" if self._direction == -1 else "minimization"
        log.info(
            "NevergradSweeper(optimizer=%s, budget=%s, num_workers=%s) %s",
            self.optimizer,
            self.budget,
            self.num_workers,
            name,
        )
        log.info("with parametrization %s", parametrization)
        log.info("Sweep output dir : %s", self.config.hydra.sweep.dir)
        optimizer = ng.optimizers.registry[self.optimizer](
            parametrization, self.budget, self.num_workers
        )
        # loop!
        remaining_budget = self.budget
        all_returns: List[Any] = []
        while remaining_budget > 0:
            batch = min(self.num_workers, remaining_budget)
            remaining_budget -= batch
            candidates = [optimizer.ask() for _ in range(batch)]
            overrides = list(
                tuple(f"{x}={y}" for x, y in c.value.items()) for c in candidates
            )
            returns = self.launcher.launch(overrides)
            # would have been nice to avoid waiting for all jobs to finish
            # aka batch size Vs steady state (launching a new job whenever one is done)
            for cand, ret in zip(candidates, returns):
                optimizer.tell(cand, self._direction * ret.return_value)
            all_returns.extend(returns)
        recom = optimizer.provide_recommendation()
        results_to_serialize = {"optimizer": "nevergrad", "nevergrad": recom.value}
        results_to_serialize = json.loads(json.dumps(results_to_serialize))
        OmegaConf.save(
            OmegaConf.create(results_to_serialize),
            f"{self.config.hydra.sweep.dir}/optimization_results.yaml",
        )
        log.info(
            "Best parameters: %s", " ".join(f"{x}={y}" for x, y in recom.value.items())
        )
