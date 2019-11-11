# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from typing import Tuple, List, Iterator, NewType

from ax import ParameterType
from ax.service.ax_client import AxClient

from hydra._internal.config_search_path import ConfigSearchPath
from hydra._internal.plugins import Plugins
from hydra.plugins import SearchPathPlugin, Sweeper

log = logging.getLogger(__name__)

Trial = NewType("Trial", List[str])

# TODO: output directory is overwriting, job.num should be adjusted
# TODO: track best value and stop when no improvement (configurable)


class AxSweeperSearchPathPlugin(SearchPathPlugin):
    """
    This plugin is allowing configuration files provided by the AxSweeper plugin to be discovered
    and used once the AxSweeper plugin is installed
    """

    def manipulate_search_path(self, search_path):
        assert isinstance(search_path, ConfigSearchPath)
        # Appends the search path for this plugin to the end of the search path
        search_path.append("hydra-ax-sweeper", "pkg://hydra_plugins.ax_sweeper.conf")


def map_params_to_arg_list(params: dict) -> List[str]:
    """Method to map a dictionary of params to a list of string arguments"""
    arg_list = []
    for key in params:
        arg_list.append(str(key) + "=" + str(params[key]))
    return arg_list


def yield_batch_of_trials_from_parallelism(
    ax: AxClient, parallelism: Tuple[int, int]
) -> Iterator[List[Trial]]:
    num_trials, num_parallel_trials = parallelism
    if num_trials == -1:
        # Special case, return infinite number of batches
        while True:
            yield get_one_batch_of_trials(ax, num_parallel_trials)
    else:
        if num_parallel_trials == -1:
            num_parallel_trials = num_trials
        number_of_parallel_trials = int(num_trials / num_parallel_trials)
        for batch_idx in range(number_of_parallel_trials):
            yield get_one_batch_of_trials(ax, num_parallel_trials)


def get_one_batch_of_trials(ax: AxClient, num_parallel_trials: int) -> List[Trial]:
    batch_of_trials = []
    for trial_idx in range(num_parallel_trials):
        parameters, trial_index = ax.get_next_trial()
        batch_of_trials.append(
            {
                "overrides": map_params_to_arg_list(params=parameters),
                "trial_index": trial_index,
            }
        )
    return batch_of_trials


def yield_batch_of_trials_from_ax(ax: AxClient, num_max_trials: int):
    recommended_max_parallelism = ax.get_recommended_max_parallelism()
    num_trials_left = num_max_trials
    for parallelism in recommended_max_parallelism:
        for batch_of_trials in yield_batch_of_trials_from_parallelism(ax, parallelism):
            yield batch_of_trials[:num_trials_left]
            num_trials_left -= len(batch_of_trials[:num_trials_left])
            if num_trials_left <= 0:
                return


def _is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class AxSweeper(Sweeper):
    def __init__(self, verbose_logging, experiment):
        self.launcher = None
        self.job_results = None
        self.experiment = experiment
        self.verbose_logging = verbose_logging

    def setup(self, config, config_loader, task_function):
        self.launcher = Plugins.instantiate_launcher(
            config=config, config_loader=config_loader, task_function=task_function
        )

    def sweep(self, arguments):
        ax = self.setup_ax_client(arguments)
        num_max_trials = 500
        for batch_of_trials in yield_batch_of_trials_from_ax(ax, num_max_trials):
            log.info("AxSweeper is launching {} jobs".format(len(batch_of_trials)))

            overrides = [x["overrides"] for x in batch_of_trials]
            rets = self.launcher.launch(overrides)
            for idx in range(len(batch_of_trials)):
                ax.complete_trial(
                    trial_index=batch_of_trials[idx]["trial_index"],
                    raw_data=rets[idx].return_value,
                )

        best = ax.get_best_parameters()
        log.info("Best parameters: " + str(best))

    def setup_ax_client(self, arguments) -> AxClient:
        parameters = []
        for s in arguments:
            key, value = s.split("=")
            if "," in value:
                # choice
                values = value.split(",")
                parameters.append(
                    {
                        "name": key,
                        "type": "choice",
                        "values": values,
                        "parameter_type": ParameterType.STRING,
                    }
                )
            elif ":" in value:
                # range
                x1, x2 = value.split(":")
                if _is_int(x1) and _is_int(x2):
                    x1 = int(x1)
                    x2 = int(x2)
                    param_type = ParameterType.INT
                else:
                    x1 = float(x1)
                    x2 = float(x2)
                    param_type = ParameterType.FLOAT
                parameters.append(
                    {
                        "name": key,
                        "type": "range",
                        "bounds": [x1, x2],
                        "parameter_type": param_type,
                    }
                )
            else:
                # fixed
                parameters.append(
                    {
                        "name": key,
                        "type": "fixed",
                        "value": value,
                        "parameter_type": ParameterType.STRING,
                    }
                )

        ax = AxClient(verbose_logging=self.verbose_logging)
        ax.create_experiment(parameters=parameters, **self.experiment)
        return ax
