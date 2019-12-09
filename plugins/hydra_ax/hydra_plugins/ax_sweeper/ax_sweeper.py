# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from typing import Iterator, List, NewType, Tuple

from ax import ParameterType
from ax.service.ax_client import AxClient
from hydra._internal.config_search_path import ConfigSearchPath
from hydra._internal.plugins import Plugins
from hydra.plugins import SearchPathPlugin, Sweeper

log = logging.getLogger(__name__)

Trial = NewType("Trial", List[str])

# TODO: output directory is overwriting, job.num should be adjusted (depends on issue #284)
# TODO: Support running multiple random seeds, aggregate mean and SEM


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
    """Produce a batch of trials that can be run in parallel, given the parallelism"""
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
    """Produce a batch of trials that can be run in parallel"""
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
    """Yield batches of trials that can be run in parallel"""
    recommended_max_parallelism = ax.get_recommended_max_parallelism()
    num_trials_left = num_max_trials
    for parallelism in recommended_max_parallelism:
        for batch_of_trials in yield_batch_of_trials_from_parallelism(ax, parallelism):
            yield batch_of_trials[:num_trials_left]
            num_trials_left -= len(batch_of_trials[:num_trials_left])
            if num_trials_left <= 0:
                return


class EarlyStopper:
    """Class to implement the early stopping mechanism.
    The optimisation process is stopped when the performance does not
    improve for a threshold number of consecutive epochs. The performance
    is considered to have improved when the change is more than a given
    threshold (epsilon)."""

    def __init__(self, max_epochs_without_improvement, epsilon, minimize):
        self.max_epochs_without_improvement = max_epochs_without_improvement
        self.epsilon = epsilon
        self.minimize = minimize
        self.current_best_value = None
        self.current_epochs_without_improvement = 0

    def should_stop(self, potential_best_value, best_parameters):
        """Check if the optimisation process should be stopped."""
        is_improving = True
        if self.current_best_value is not None:
            if self.minimize:
                is_improving = (
                    potential_best_value + self.epsilon < self.current_best_value
                )
            else:
                is_improving = (
                    potential_best_value - self.epsilon > self.current_best_value
                )

        if is_improving:
            self.current_epochs_without_improvement = 0
            self.current_best_value = potential_best_value
            log.info(
                "New best value: {}, best parameters: {}".format(
                    potential_best_value, best_parameters
                )
            )

            return False
        else:
            self.current_epochs_without_improvement += 1

        if (
            self.current_epochs_without_improvement
            >= self.max_epochs_without_improvement
        ):
            log.info(
                "Early stopping, best known value {} did not improve for {} epochs".format(
                    self.current_best_value, self.current_epochs_without_improvement
                )
            )
            return True
        return False


class AxSweeper(Sweeper):
    """Class to interface with the Ax Platform"""

    def __init__(
        self, verbose_logging, experiment, early_stop, random_seed, max_trials
    ):
        self.launcher = None
        self.job_results = None
        self.experiment = experiment
        self.early_stopper = EarlyStopper(**early_stop)
        self.verbose_logging = verbose_logging
        self.random_seed = random_seed
        self.max_trials = max_trials

    def setup(self, config, config_loader, task_function):
        self.launcher = Plugins.instantiate_launcher(
            config=config, config_loader=config_loader, task_function=task_function
        )

    def sweep(self, arguments):
        ax_client = self.setup_ax_client(arguments)
        for batch_of_trials in yield_batch_of_trials_from_ax(
            ax_client, self.max_trials
        ):
            log.info("AxSweeper is launching {} jobs".format(len(batch_of_trials)))

            overrides = [x["overrides"] for x in batch_of_trials]
            rets = self.launcher.launch(overrides)
            for idx in range(len(batch_of_trials)):
                val = rets[idx].return_value
                ax_client.complete_trial(
                    trial_index=batch_of_trials[idx]["trial_index"], raw_data=val
                )
            # predicted best value
            best = ax_client.get_best_parameters()
            metric = best[1][0][ax_client.objective_name]
            if self.early_stopper.should_stop(metric, best[0]):
                break

        log.info("Best parameters: " + str(best))

    def setup_ax_client(self, arguments) -> AxClient:
        """Method to setup the Ax Client"""

        def _is_int(string_inp):
            """Method to check if the given string input can be parsed as integer"""
            try:
                int(string_inp)
                return True
            except ValueError:
                return False

        parameters = []
        for arg in arguments:
            key, value = arg.split("=")
            if "," in value:
                # This is a Choice Parameter.
                value_choices = value.split(",")
                parameters.append(
                    {
                        "name": key,
                        "type": "choice",
                        "values": value_choices,
                        "parameter_type": ParameterType.STRING,
                    }
                )
            elif ":" in value:
                # This is a Range Parameter.
                range_start, range_end = value.split(":")
                if _is_int(range_start) and _is_int(range_end):
                    range_start = int(range_start)
                    range_end = int(range_end)
                    param_type = ParameterType.INT
                else:
                    range_start = float(range_start)
                    range_end = float(range_end)
                    param_type = ParameterType.FLOAT
                parameters.append(
                    {
                        "name": key,
                        "type": "range",
                        "bounds": [range_start, range_end],
                        "parameter_type": param_type,
                    }
                )
            else:
                # This is a Fixed Parameter.
                parameters.append(
                    {
                        "name": key,
                        "type": "fixed",
                        "value": value,
                        "parameter_type": ParameterType.STRING,
                    }
                )

        ax_client = AxClient(
            verbose_logging=self.verbose_logging, random_seed=self.random_seed
        )
        ax_client.create_experiment(parameters=parameters, **self.experiment)
        return ax_client
