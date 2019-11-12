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


class EarlyStopper:
    def __init__(self, max_epochs_without_improvement, epsilon, minimize):
        self.max_epochs_without_improvement = max_epochs_without_improvement
        self.epsilon = epsilon
        self.minimize = minimize
        self.current_known_best = None
        self.current_epochs_without_improvement = 0

    def should_stop(self, current_best, best_parameters):
        improve = True
        if self.current_known_best is not None:
            if self.minimize:
                improve = current_best + self.epsilon < self.current_known_best
            else:
                improve = current_best - self.epsilon > self.current_known_best

        if improve:
            self.current_epochs_without_improvement = 0
            self.current_known_best = current_best
            log.info(
                "New best : {}, parameters: {}".format(current_best, best_parameters)
            )

            return False
        else:
            self.current_epochs_without_improvement += 1

        if (
            self.current_epochs_without_improvement
            >= self.max_epochs_without_improvement
        ):
            log.info(
                "Early stopping, best known {} did not improve for {} epochs".format(
                    self.current_known_best, self.current_epochs_without_improvement
                )
            )
            return True


class AxSweeper(Sweeper):
    def __init__(self, verbose_logging, experiment, early_stop):
        self.launcher = None
        self.job_results = None
        self.experiment = experiment
        self.early_stopper = EarlyStopper(**early_stop)
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
                val = rets[idx].return_value
                ax.complete_trial(
                    trial_index=batch_of_trials[idx]["trial_index"], raw_data=val
                )
            best = ax.get_best_parameters()

            metric = best[1][0][ax.objective_name]
            if self.early_stopper.should_stop(metric, best[0]):
                break

        log.info("Best parameters: " + str(best))

    def setup_ax_client(self, arguments) -> AxClient:
        def _is_int(ss):
            try:
                int(ss)
                return True
            except ValueError:
                return False

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
