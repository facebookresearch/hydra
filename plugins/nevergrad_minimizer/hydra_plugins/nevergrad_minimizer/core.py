# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import itertools
import logging
import typing as tp
import nevergrad as ng

from omegaconf import DictConfig

from hydra.core.config_loader import ConfigLoader
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.plugins.search_path_plugin import SearchPathPlugin
from hydra.plugins.sweeper import Sweeper
from hydra.types import TaskFunction

log = logging.getLogger(__name__)


class NgSearchPathPlugin(SearchPathPlugin):
    """
    This plugin is allowing configuration files provided by the ExampleSweeper plugin to be discovered
    and used once the ExampleSweeper plugin is installed
    """

    def manipulate_search_path(self, search_path: ConfigSearchPath) -> None:
        # Appends the search path for this plugin to the end of the search path
        search_path.append(
            "nevergrad-minimizer", "pkg://hydra_plugins.nevergrad_minimizer.conf"
        )


def read_value(string: str) -> tp.Union[int, float, str]:
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
    output: tp.Union[float, int, str] = string
    try:
        output = float(string)
    except ValueError:
        pass
    else:
        if output.is_integer() and "." not in string:
            output = int(output)
    return output


def make_parameter(string: str) -> tp.Union[int, float, str, ng.p.Parameter]:
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
        choices = [read_value(x) for x in string.split(",")]
        ordered = all(isinstance(c, (int, float)) for c in choices)
        ordered &= all(c0 <= c1 for c0, c1 in zip(choices[:-1], choices[1:]))  # type: ignore
        return (ng.p.TransitionChoice if ordered else ng.p.Choice)(choices)  # type: ignore
    if ":" in string:
        a, b = [read_value(x) for x in string.split(":")]
        assert all(isinstance(c, (int, float)) for c in (a, b)), "Bounds must be scalars"
        sigma = (b - a) / 6  # type: ignore
        scalar = ng.p.Scalar(init=(a + b) / 2.0).set_bounds(  # type: ignore
            a_min=a, a_max=b, full_range_sampling=True
        ).set_mutation(sigma=sigma)
        if all(isinstance(c, int) for c in (a, b)):
            scalar.set_integer_casting()
        return scalar
    return read_value(string)  # constant


class NevergradMinimizer(Sweeper):
    def __init__(self, optimizer: str, budget: int, num_workers: int, noisy: bool, version: int):
        self.config: tp.Optional[DictConfig] = None
        self.launcher: tp.Optional[Launcher] = None
        assert version == 1, "Only version 1 of API is currently available"
        self.job_results = None
        self.optimizer = optimizer
        self.noisy = noisy
        self.budget = budget
        self.num_workers = num_workers

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

    def sweep(self, arguments: tp.List[str]) -> tp.Any:
        assert self.config is not None
        assert self.launcher is not None
        # Construct the parametrization
        params: tp.Dict[str, tp.Union[str, int, float, ng.p.Parameter]] = {}
        for s in arguments:
            key, value = s.split("=", 1)
            params[key] = make_parameter(value)
        instrumentation = ng.p.Instrumentation(**params)
        instrumentation.descriptors.deterministic_function = not self.noisy
        # log and build the optimizer
        log.info("NevergradMinimizer(optimizer=%s, budget=%s, num_workers=%s) sweeping",
                 self.optimizer, self.budget, self.num_workers)
        log.info("with %s", instrumentation)
        log.info("Sweep output dir : %s", self.config.hydra.sweep.dir)
        optimizer = ng.optimizers.registry[self.optimizer](instrumentation, self.budget, self.num_workers)
        # loop!
        remaining_budget = self.budget
        all_returns: tp.List[tp.Any] = []
        while remaining_budget > 0:
            batch = min(self.num_workers, remaining_budget)
            remaining_budget -= batch
            candidates = [optimizer.ask() for _ in range(batch)]
            overrides = list(tuple(f"{x}={y}" for x, y in c.kwargs.items()) for c in candidates)
            returns = self.launcher.launch(overrides)
            # would have been nice to avoid waiting for all jobs to finish
            # aka batch size Vs steady state (launching a new job whenever one is done)
            for cand, ret in zip(candidates, returns):
                optimizer.tell(cand, ret.return_value)
            all_returns.extend(returns)
        return all_returns  # not sure what the return should be
