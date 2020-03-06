# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import json
import logging
from typing import Any, Dict, List, Optional, Union

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
    if not isinstance(string, str):
        return string
    try:
        output = float(string)
    except ValueError:
        pass
    else:
        if output.is_integer() and "." not in string:
            output = int(output)
    return output


def _make_list_parameter(param_list: List[str]) -> Any:
    import nevergrad as ng  # type: ignore

    choices = [convert_to_deduced_type(x) for x in param_list]
    print(choices)
    ordered = all(isinstance(c, (int, float)) for c in choices)
    ordered &= all(
        c0 <= c1 for c0, c1 in zip(choices[:-1], choices[1:])  # type: ignore
    )
    return ng.p.TransitionChoice(choices) if ordered else ng.p.Choice(choices)


def make_parameter_from_commandline(string: str) -> Any:
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
         - ":log:"-separated values for ranges of log-distributed positive scalars.
           Eg.: "0.001:log:1.0"
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
    import nevergrad as ng

    string = string.strip()
    if string.startswith(tuple(dir(ng.p))):
        param = eval("ng.p." + string)  # pylint: disable=eval-used
        assert isinstance(param, ng.p.Parameter)
        return param
    if "," in string:
        return _make_list_parameter(string.split(","))
    for sep in [":log:", ":"]:
        if sep in string:
            a, b = [convert_to_deduced_type(x) for x in string.split(sep)]
            assert isinstance(a, (int, float)), "Bounds must be scalars"
            assert isinstance(b, (int, float)), "Bounds must be scalars"
            if sep == ":":
                sigma = (b - a) / 6
                scalar = (
                    ng.p.Scalar(init=(a + b) / 2.0)
                    .set_mutation(sigma=sigma)
                    .set_bounds(a_min=a, a_max=b, full_range_sampling=True)
                )
            else:
                scalar = ng.p.Log(a_min=a, a_max=b)
            if all(isinstance(c, int) for c in (a, b)):
                if b - a <= 6:
                    raise ValueError(
                        "For integers with 6 or fewer values, use a choice instead"
                    )
                scalar.set_integer_casting()
            return scalar
    return convert_to_deduced_type(string)  # constant


def make_parameter_from_config(description: Any) -> Any:
    import nevergrad as ng

    if isinstance(description, ListConfig):
        return _make_list_parameter(list(description))
    elif isinstance(description, str) and description.startswith(tuple(dir(ng.p))):
        param = eval("ng.p." + description)  # pylint: disable=eval-used
        assert isinstance(param, ng.p.Parameter)
        return param
    elif isinstance(description, DictConfig):
        init = ["init", "lower", "upper"]
        options = init + ["log", "step"]
        assert all(x in options for x in description)
        init_params = {x: y for x, y in description.items() if x in init}
        if description.get("log", False):
            param = ng.p.Scalar(**init_params)
            if "step" in description:
                param.set_mutation(sigma=description["step"])
        else:
            if "step" in description:
                init_params["exponent"] = description["step"]
            param = ng.p.Log(**init_params)
            return param
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
        assert version == 1, "Only version 1 of API is currently available"
        self.opt_config = optim
        self.config: Optional[DictConfig] = None
        self.launcher: Optional[Launcher] = None
        self.job_results = None
        self.parametrization: Dict[str, Any] = {}
        if parametrization is not None:
            print(parametrization)
            assert isinstance(parametrization, DictConfig)
            self.parametrization = {
                x: make_parameter_from_config(y) for x, y in parametrization.items()
            }

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
        import nevergrad as ng

        assert self.config is not None
        assert self.launcher is not None
        direction = -1 if self.opt_config.maximize else 1
        name = "maximization" if self.opt_config.maximize else "minimization"
        # Construct the parametrization
        params: Dict[str, Union[str, int, float, ng.p.Parameter]] = {}
        for s in arguments:
            key, value = s.split("=", 1)
            params[key] = make_parameter_from_commandline(value)
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
        while remaining_budget > 0:
            batch = min(nw, remaining_budget)
            remaining_budget -= batch
            candidates = [optimizer.ask() for _ in range(batch)]
            overrides = list(
                tuple(f"{x}={y}" for x, y in c.value.items()) for c in candidates
            )
            returns = self.launcher.launch(overrides)
            # would have been nice to avoid waiting for all jobs to finish
            # aka batch size Vs steady state (launching a new job whenever one is done)
            for cand, ret in zip(candidates, returns):
                optimizer.tell(cand, direction * ret.return_value)
            all_returns.extend(returns)
        recom = optimizer.provide_recommendation()
        results_to_serialize = {"optimizer": "nevergrad", "nevergrad": recom.value}
        # TODO remove the following line with next nevergrad release
        results_to_serialize = json.loads(json.dumps(results_to_serialize))
        OmegaConf.save(
            OmegaConf.create(results_to_serialize),
            f"{self.config.hydra.sweep.dir}/optimization_results.yaml",
        )
        log.info(
            "Best parameters: %s", " ".join(f"{x}={y}" for x, y in recom.value.items())
        )
