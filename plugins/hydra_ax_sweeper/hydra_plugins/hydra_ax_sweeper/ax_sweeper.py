# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from typing import List, Tuple

from ax import ParameterType
from ax.service.ax_client import AxClient
from omegaconf import OmegaConf

from hydra._internal.config_search_path import ConfigSearchPath
from hydra._internal.plugins import Plugins
from hydra.plugins import SearchPathPlugin, Sweeper

log = logging.getLogger(__name__)

Trial = List[str]
BatchOfTrial = List[Trial]

# TODO: output directory is overwriting, job.num should be adjusted (depends on issue #284)
# TODO: Support running multiple random seeds, aggregate mean and SEM


class AxSweeperSearchPathPlugin(SearchPathPlugin):
    """
    This plugin makes the config files (provided by the AxSweeper plugin) discoverable and
    useable by the AxSweeper plugin.
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


def get_batches_of_trials_given_parallelism(
    ax: AxClient, parallelism: Tuple[int, int], num_trials_left: int
) -> List[BatchOfTrial]:
    """Produce a batch of trials that can be run in parallel, given the parallelism"""
    num_trials, num_parallel_trials = parallelism
    if num_trials == -1:
        # This is a special case. We can use this parallelism as many times as we want.

        if num_parallel_trials == -1:
            # This is another special case where we can run as many trials in parallel as we want.
            # Given that num_trials is also -1, we can run all the trials in parallel.
            num_parallel_trials = num_trials_left
        while True:
            yield get_one_batch_of_trials(ax, num_parallel_trials)
    else:
        if num_parallel_trials == -1:
            num_parallel_trials = num_trials
        number_of_parallel_trials = int(num_trials / num_parallel_trials)
        for batch_idx in range(number_of_parallel_trials):
            yield get_one_batch_of_trials(ax, num_parallel_trials)


def get_one_batch_of_trials(ax: AxClient, num_parallel_trials: int) -> BatchOfTrial:
    """Produce a batch of trials that can be run in parallel"""
    batch_of_trials = []
    for _ in range(num_parallel_trials):
        parameters, trial_index = ax.get_next_trial()
        batch_of_trials.append(
            {
                "overrides": map_params_to_arg_list(params=parameters),
                "trial_index": trial_index,
            }
        )
    return batch_of_trials


def get_batches_of_trials_from_ax(
    ax: AxClient, num_max_trials: int
) -> List[BatchOfTrial]:
    """Return a list of batch of trials that can be run in parallel"""
    list_of_batch_of_trials = []
    recommended_max_parallelism = ax.get_recommended_max_parallelism()
    print(recommended_max_parallelism)
    num_trials_left = num_max_trials
    for parallelism in recommended_max_parallelism:
        for batch_of_trials in get_batches_of_trials_given_parallelism(
            ax, parallelism, num_trials_left
        ):
            list_of_batch_of_trials.append(batch_of_trials[:num_trials_left])
            num_trials_left -= len(list_of_batch_of_trials[-1])
            if num_trials_left <= 0:
                return list_of_batch_of_trials
    return list_of_batch_of_trials


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
        self,
        verbose_logging,
        experiment,
        early_stop,
        random_seed,
        max_trials,
        ax_params,
    ):
        self.launcher = None
        self.job_results = None
        self.experiment = experiment
        self.early_stopper = EarlyStopper(**early_stop)
        self.verbose_logging = verbose_logging
        self.random_seed = random_seed
        self.max_trials = max_trials
        self.ax_params = ax_params

    def setup(self, config, config_loader, task_function):
        self.launcher = Plugins.instantiate_launcher(
            config=config, config_loader=config_loader, task_function=task_function
        )

    def sweep(self, arguments):
        ax_client = self.setup_ax_client(arguments)

        for batch_of_trials in get_batches_of_trials_from_ax(
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

        parameters = []
        for key, value in self.ax_params.items():
            parameters.append(OmegaConf.to_container(value, resolve=True))
            parameters[-1]["name"] = key
        commandline_params = self.parse_commandline_args(arguments)
        for cmd_param in commandline_params:
            for param in parameters:
                if param["name"] == cmd_param["name"]:
                    for key, value in cmd_param.items():
                        param[key] = value
        ax_client = AxClient(
            verbose_logging=self.verbose_logging, random_seed=self.random_seed
        )
        ax_client.create_experiment(parameters=parameters, **self.experiment)

        return ax_client

    def parse_commandline_args(self, arguments):
        """Method to parse the command line arguments and convert them into Ax parameters"""

        def _is_int(string_inp):
            """Method to check if the given string input can be parsed as integer"""
            try:
                int(string_inp)
                return True
            except ValueError:
                return False

        def _is_float(string_inp):
            """Method to check if the given string input can be parsed as a float"""
            try:
                float(string_inp)
                return True
            except ValueError:
                return False

        parameters = []
        for arg in arguments:
            key, value = arg.split("=")
            if "," in value:
                # This is a Choice Parameter.

                value_choices = [x for x in value.split(",")]
                if _is_float(value_choices[0]):
                    parameter_type = ParameterType.FLOAT
                    value_choices = [float(x) for x in value_choices]
                else:
                    parameter_type = ParameterType.STRING
                parameters.append(
                    {
                        "name": key,
                        "type": "choice",
                        "values": value_choices,
                        "parameter_type": parameter_type,
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

        return parameters
