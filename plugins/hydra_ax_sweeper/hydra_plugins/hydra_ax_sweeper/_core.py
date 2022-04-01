# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple, Union

from ax.core import types as ax_types  # type: ignore
from ax.exceptions.core import SearchSpaceExhausted  # type: ignore
from ax.service.ax_client import AxClient  # type: ignore
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.override_parser.types import IntervalSweep, Override, Transformer
from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.plugins.sweeper import Sweeper
from hydra.types import HydraContext, TaskFunction
from omegaconf import DictConfig, OmegaConf

from ._earlystopper import EarlyStopper
from .config import AxConfig, ClientConfig, ExperimentConfig

log = logging.getLogger(__name__)


@dataclass
class Trial:
    overrides: List[str]
    trial_index: int


@dataclass
class TrialBatch:
    list_of_trials: List[Trial]
    is_search_space_exhausted: bool


def encoder_parameters_into_string(parameters: List[Dict[str, Any]]) -> str:
    """Convert a list of params into a string"""
    mandatory_keys = set(["name", "type", "bounds", "values", "value"])
    parameter_log_string = ""
    for parameter in parameters:
        parameter_log_string += "\n"
        parameter_log_string += f"{parameter['name']}: {parameter['type']}="
        if parameter["type"] == "range":
            parameter_log_string += f"{parameter['bounds']}"
        elif parameter["type"] == "choice":
            parameter_log_string += f"{parameter['values']}"
        elif parameter["type"] == "fixed":
            parameter_log_string += f"{parameter['value']}"

        for key, value in parameter.items():
            if key not in mandatory_keys:
                parameter_log_string += f", {key} = {value}"
    return parameter_log_string


def map_params_to_arg_list(params: Mapping[str, Union[str, float, int]]) -> List[str]:
    """Method to map a dictionary of params to a list of string arguments"""
    arg_list = []
    for key in params:
        arg_list.append(str(key) + "=" + str(params[key]))
    return arg_list


def get_one_batch_of_trials(
    ax_client: AxClient,
    parallelism: Tuple[int, int],
    num_trials_so_far: int,
    num_max_trials_to_do: int,
) -> TrialBatch:
    """Returns a TrialBatch that contains a list of trials that can be
    run in parallel. TrialBatch also flags if the search space is exhausted."""

    is_search_space_exhausted = False
    # Ax throws an exception if the search space is exhausted. We catch
    # the exception and set the flag to True
    (num_trials, max_parallelism_setting) = parallelism
    if max_parallelism_setting == -1:
        # Special case, we can group all the trials into one batch
        max_parallelism_setting = num_trials - num_trials_so_far

        if num_trials == -1:
            # This is a special case where we can run as many trials in parallel as we want.
            # Given that num_trials is also -1, we can run all the trials in parallel.
            max_parallelism_setting = num_max_trials_to_do

    list_of_trials = []
    for _ in range(max_parallelism_setting):
        try:
            parameters, trial_index = ax_client.get_next_trial()
            list_of_trials.append(
                Trial(
                    overrides=map_params_to_arg_list(params=parameters),
                    trial_index=trial_index,
                )
            )
        except SearchSpaceExhausted:
            is_search_space_exhausted = True
            break

    return TrialBatch(
        list_of_trials=list_of_trials,
        is_search_space_exhausted=is_search_space_exhausted,
    )


class CoreAxSweeper(Sweeper):
    """Class to interface with the Ax Platform"""

    def __init__(self, ax_config: AxConfig, max_batch_size: Optional[int]):
        self.config: Optional[DictConfig] = None
        self.launcher: Optional[Launcher] = None
        self.hydra_context: Optional[HydraContext] = None

        self.job_results = None
        self.experiment: ExperimentConfig = ax_config.experiment
        self.early_stopper: EarlyStopper = EarlyStopper(
            max_epochs_without_improvement=ax_config.early_stop.max_epochs_without_improvement,
            epsilon=ax_config.early_stop.epsilon,
            minimize=ax_config.early_stop.minimize,
        )
        self.ax_client_config: ClientConfig = ax_config.client
        self.max_trials = ax_config.max_trials
        self.ax_params: DictConfig = OmegaConf.create({})
        if hasattr(ax_config, "params"):
            self.ax_params.update(ax_config.params)
        self.sweep_dir: str
        self.job_idx: Optional[int] = None
        self.max_batch_size = max_batch_size
        self.is_noisy: bool = ax_config.is_noisy

    def setup(
        self,
        *,
        hydra_context: HydraContext,
        task_function: TaskFunction,
        config: DictConfig,
    ) -> None:
        self.config = config
        self.hydra_context = hydra_context
        self.launcher = Plugins.instance().instantiate_launcher(
            config=config, hydra_context=hydra_context, task_function=task_function
        )
        self.sweep_dir = config.hydra.sweep.dir

    def sweep(self, arguments: List[str]) -> None:
        self.job_idx = 0
        ax_client = self.setup_ax_client(arguments)

        num_trials_left = self.max_trials
        max_parallelism = ax_client.get_max_parallelism()
        current_parallelism_index = 0
        # Index to track the parallelism value we are using right now.
        is_search_space_exhausted = False
        # Ax throws an exception if the search space is exhausted. We catch
        # the exception and set the flag to True

        best_parameters = {}
        while num_trials_left > 0 and not is_search_space_exhausted:
            current_parallelism = max_parallelism[current_parallelism_index]
            num_trials, max_parallelism_setting = current_parallelism
            num_trials_so_far = 0
            while (
                num_trials > num_trials_so_far or num_trials == -1
            ) and num_trials_left > 0:
                trial_batch = get_one_batch_of_trials(
                    ax_client=ax_client,
                    parallelism=current_parallelism,
                    num_trials_so_far=num_trials_so_far,
                    num_max_trials_to_do=num_trials_left,
                )

                list_of_trials_to_launch = trial_batch.list_of_trials[:num_trials_left]
                is_search_space_exhausted = trial_batch.is_search_space_exhausted

                log.info(
                    "AxSweeper is launching {} jobs".format(
                        len(list_of_trials_to_launch)
                    )
                )

                self.sweep_over_batches(
                    ax_client=ax_client, list_of_trials=list_of_trials_to_launch
                )

                num_trials_so_far += len(list_of_trials_to_launch)
                num_trials_left -= len(list_of_trials_to_launch)

                best_parameters, predictions = ax_client.get_best_parameters()
                metric = predictions[0][ax_client.objective_name]

                if self.early_stopper.should_stop(metric, best_parameters):
                    num_trials_left = -1
                    break

                if is_search_space_exhausted:
                    log.info("Ax has exhausted the search space")
                    break

            current_parallelism_index += 1

        results_to_serialize = {"optimizer": "ax", "ax": best_parameters}
        OmegaConf.save(
            OmegaConf.create(results_to_serialize),
            f"{self.sweep_dir}/optimization_results.yaml",
        )
        log.info("Best parameters: " + str(best_parameters))

    def sweep_over_batches(
        self, ax_client: AxClient, list_of_trials: List[Trial]
    ) -> None:
        assert self.launcher is not None
        assert self.job_idx is not None

        chunked_batches = self.chunks(list_of_trials, self.max_batch_size)
        for batch in chunked_batches:
            overrides = [x.overrides for x in batch]
            self.validate_batch_is_legal(overrides)
            rets = self.launcher.launch(
                job_overrides=overrides, initial_job_idx=self.job_idx
            )
            self.job_idx += len(rets)
            for idx in range(len(batch)):
                val: Any = rets[idx].return_value
                # Ax expects a measured value (int or float), which can optionally
                # be given in a tuple along with the error of that measurement
                assert isinstance(val, (int, float, tuple))
                # is_noisy specifies how Ax should behave when not given an error value.
                # if true (default), the error of each measurement is inferred by Ax.
                # if false, the error of each measurement is set to 0.
                if isinstance(val, (int, float)):
                    if self.is_noisy:
                        val = (val, None)  # specify unknown noise
                    else:
                        val = (val, 0)  # specify no noise
                ax_client.complete_trial(
                    trial_index=batch[idx].trial_index, raw_data=val
                )

    def setup_ax_client(self, arguments: List[str]) -> AxClient:
        """Method to setup the Ax Client"""
        parameters: List[Dict[Any, Any]] = []
        for key, value in self.ax_params.items():
            param = OmegaConf.to_container(value, resolve=True)
            assert isinstance(param, Dict)
            if param["type"] == "range":
                bounds = param["bounds"]
                if not (all(isinstance(x, int) for x in bounds)):
                    # Type mismatch. Promote all to float
                    param["bounds"] = [float(x) for x in bounds]

            parameters.append(param)
            parameters[-1]["name"] = key
        commandline_params = self.parse_commandline_args(arguments)
        for cmd_param in commandline_params:
            for param in parameters:
                if param["name"] == cmd_param["name"]:
                    for key, value in cmd_param.items():
                        param[key] = value
                    break
            else:
                parameters.append(cmd_param)

        log.info(
            f"AxSweeper is optimizing the following parameters: {encoder_parameters_into_string(parameters)}"
        )
        ax_client = AxClient(
            verbose_logging=self.ax_client_config.verbose_logging,
            random_seed=self.ax_client_config.random_seed,
        )
        ax_client.create_experiment(parameters=parameters, **self.experiment)

        return ax_client

    def parse_commandline_args(
        self, arguments: List[str]
    ) -> List[Dict[str, Union[ax_types.TParamValue, List[ax_types.TParamValue]]]]:
        """Method to parse the command line arguments and convert them into Ax parameters"""
        parser = OverridesParser.create()
        parsed = parser.parse_overrides(arguments)
        parameters: List[Dict[str, Any]] = []
        for override in parsed:
            if override.is_sweep_override():
                if override.is_choice_sweep():
                    param = create_choice_param_from_choice_override(override)
                elif override.is_range_sweep():
                    param = create_choice_param_from_range_override(override)
                elif override.is_interval_sweep():
                    param = create_range_param_using_interval_override(override)
            elif not override.is_hydra_override():
                param = create_fixed_param_from_element_override(override)
            parameters.append(param)

        return parameters

    @staticmethod
    def chunks(batch: List[Any], n: Optional[int]) -> Iterable[List[Any]]:
        """
        Chunk the batch into chunks of upto to n items (each)
        """
        if n is None:
            n = len(batch)
        if n < 1:
            raise ValueError("n must be an integer greater than 0")
        for i in range(0, len(batch), n):
            yield batch[i : i + n]


def create_range_param_using_interval_override(override: Override) -> Dict[str, Any]:
    key = override.get_key_element()
    value = override.value()
    assert isinstance(value, IntervalSweep)
    param = {
        "name": key,
        "type": "range",
        "bounds": [value.start, value.end],
        "log_scale": "log" in value.tags,
    }
    return param


def create_choice_param_from_choice_override(override: Override) -> Dict[str, Any]:
    key = override.get_key_element()
    param = {
        "name": key,
        "type": "choice",
        "values": list(override.sweep_iterator(transformer=Transformer.encode)),
    }
    return param


def create_choice_param_from_range_override(override: Override) -> Dict[str, Any]:
    key = override.get_key_element()
    param = {
        "name": key,
        "type": "choice",
        "values": [val for val in override.sweep_iterator()],
    }

    return param


def create_fixed_param_from_element_override(override: Override) -> Dict[str, Any]:
    key = override.get_key_element()
    param = {
        "name": key,
        "type": "fixed",
        "value": override.value(),
    }

    return param
