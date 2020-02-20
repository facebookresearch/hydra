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
        bounds = [read_value(x) for x in string.split(":")]
        assert all(isinstance(b, (int, float)) for b in bounds), "Bounds must be scalars"
        # TODO modify to Scalar with updated API
        scalar = ng.p.Log(a_min=bounds[0], a_max=bounds[1])  # type: ignore
        if all(isinstance(b, int) for b in bounds):
            scalar.set_integer_casting()
        return scalar
    return read_value(string)  # constant


class NevergradMinimizer(Sweeper):
    def __init__(self, optimizer: str, budget: int, num_workers: int):
        self.config: tp.Optional[DictConfig] = None
        self.launcher: tp.Optional[Launcher] = None
        self.job_results = None
        self.optimizer = optimizer
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
        log.info("NevergradMinimizer(optimizer=%s, budget=%s, num_workers=%s) sweeping",
                 self.optimizer, self.budget, self.num_workers)
        log.info("Sweep output dir : %s", self.config.hydra.sweep.dir)
        # Construct list of overrides per job we want to launch
        params: tp.Dict[str, tp.Union[str, int, float, ng.p.Parameter]] = {}
        for s in arguments:
            key, value = s.split("=")
            # for each argument, create a list. if the argument has , (aka - is a sweep), add an element for each
            # option to that list, otherwise add a single element with the value
            params[key] = make_parameter(value)
        instrumentation = ng.p.Instrumentation(**params)
        log.info("Minimizing with %s", instrumentation)
        optimizer = ng.optimizers.registry[self.optimizer](instrumentation, self.budget, self.num_workers)

        candidates = [optimizer.ask() for _ in range(self.budget)]
        overrides = list(tuple(f"{x}={y}" for x, y in c.kwargs.items()) for c in candidates)
        returns = [self.launcher.launch(overrides)]
        return returns
