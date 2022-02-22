# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import asdict
import logging
from typing import List, Optional, Sequence
import os

from hydra.core import utils
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.override_parser.types import Override
from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.plugins.sweeper import Sweeper
from hydra.types import HydraContext, TaskFunction
from hydra.core.utils import JobReturn

from omegaconf import DictConfig, OmegaConf

from orion.core.utils.flatten import flatten
from orion.client import create_experiment
from orion.client.experiment import ExperimentClient
from orion.core.worker.trial import Trial, AlreadyReleased
from orion.algo.space import Space, Dimension
from orion.core.io.space_builder import DimensionBuilder, SpaceBuilder
from orion.core.utils.exceptions import (
    CompletedExperiment,
    ReservationRaceCondition,
    WaitingForTrials,
    BrokenExperiment,
    InvalidResult,
)

from .config import OrionClientConf, WorkerConf, AlgorithmConf, StorageConf

log = logging.getLogger(__name__)


def as_overrides(trial, additional):
    """Returns the trial arguments as hydra overrides"""
    kwargs = deepcopy(additional)
    kwargs.update(flatten(trial.params))
    return tuple(f"{k}={v}" for k, v in kwargs.items())


def to_objective(value):
    """Convert a return value into an Orion objective"""

    if isinstance(value, (float, int)):
        return [dict(name="objective", type="objective", value=value)]

    if isinstance(value, dict):
        return [value]

    if isinstance(value, (list, tuple)):
        return value

    raise InvalidResult(
        f"Value '{value}' of type '{str(type(value))}' is not an expected return type"
    )


class SpaceParser:
    """Generate an Orion space from parameters and overrides"""

    def __init__(self) -> None:
        self.base_space = dict()
        self.overrides = dict()
        self.arguments = dict()

    def space(self) -> Space:
        """Generate the final space after overrides that will be used for the optimization"""
        configuration = deepcopy(self.base_space)
        configuration.update(self.overrides)
        return SpaceBuilder().build(configuration), self.arguments

    def add_from_parametrization(self, parametrization: Optional[DictConfig]) -> None:
        """Use the parametrization retrieved from the configuration to generate a
        preliminary research space

        """
        for k, v in parametrization.items():
            try:
                dim = DimensionBuilder().build(k, v)
                self.base_space[dim.name] = dim.get_prior_string()
            except (TypeError, NameError):
                # Regular argument
                self.arguments[k] = v

    def add_from_overrides(self, arguments: List[str]) -> None:
        """Create a dictionary of overrides to modify the research space"""
        parser = OverridesParser.create()
        parsed = parser.parse_overrides(arguments)

        for override in parsed:
            dim = self.process_overrides(override)

            if dim is None:
                self.arguments[override.get_key_element()] = override.value()
            else:
                self.overrides[dim.name] = dim.get_prior_string()

    def process_overrides(self, override: Override) -> Dimension:
        """Identify the sweep overrides and build a matching dimension"""
        values = override.value()
        name = override.get_key_element()

        def build_dim(name):
            builder = DimensionBuilder()
            builder.name = name
            return builder

        if override.is_choice_sweep():
            return build_dim(name).choices(*values.list)

        elif override.is_range_sweep():
            if values.step == 1:
                return build_dim(name).uniform(values.start, values.stop, discrete=True)

            choices = [
                v for v in range(values.start, values.stop + values.step, values.step)
            ]
            return build_dim(name).choices(*choices)

        elif override.is_interval_sweep():
            discrete = type(values.start) is int
            log = "log" in values.tags

            cast_type = float
            if discrete or values.start % 1 == values.end % 1 == 0.0:
                cast_type = int

            method = build_dim(name).uniform
            if log:
                method = build_dim(name).loguniform

            return method(
                cast_type(values.start), cast_type(values.end), discrete=discrete
            )
        else:
            try:
                # Not sweep override but could still be orion
                return DimensionBuilder().build(name, values)
            except (TypeError, NameError):
                # Not a hyperparameter space definition
                pass


@contextmanager
def clientctx(client):
    try:
        yield client
    finally:
        client.close()


class OrionSweeperImpl(Sweeper):
    def __init__(
        self,
        orion: OrionClientConf,
        worker: WorkerConf,
        algorithm: AlgorithmConf,
        storage: StorageConf,
        parametrization: Optional[DictConfig],
    ):
        self.orion_config = orion
        self.worker_config = worker
        self.algo_config = algorithm
        self.storage_config = storage

        self.launcher: Optional[Launcher] = None
        self.hydra_context: Optional[HydraContext] = None
        self.job_results = None
        self.job_idx: Optional[int] = None

        self.space_parser = SpaceParser()
        self.space_parser.add_from_parametrization(parametrization)

    def setup(
        self,
        *,
        hydra_context: HydraContext,
        task_function: TaskFunction,
        config: DictConfig,
    ) -> None:
        self.job_idx = 0
        self.config = config
        self.hydra_context = hydra_context
        self.pending_trials = set()

        self.space = None
        self.arguments = dict()

        log.debug("Starting launcher")

        self.launcher = Plugins.instance().instantiate_launcher(
            hydra_context=hydra_context, task_function=task_function, config=config
        )

    def working_directory(self):
        return self.config.hydra.sweep.dir

    def n_workers(self):
        n = self.worker_config.n_workers
        if n <= 0:
            return os.cpu_count()

        return n

    def suggest_trials(self, count) -> List[Trial]:
        """Suggest a bunch of trials to be dispatched to the workers"""
        trials = []

        for _ in range(count):
            try:
                trial = self.client.suggest(pool_size=count)
                trials.append(trial)

            # non critical errors
            except WaitingForTrials:
                break

            except ReservationRaceCondition:
                break

            except CompletedExperiment:
                break

        return trials

    def new_experiment(self, arguments) -> ExperimentClient:
        """Initialize orion client from the config and the arguments"""

        self.space_parser.add_from_overrides(arguments)
        self.space, self.arguments = self.space_parser.space()

        dict_config = OmegaConf.to_container(self.algo_config)
        algo_type = dict_config.pop("type", "random")
        algo_config = dict_config.pop("config", dict())

        log.info("Orion Optimizer %s", self.algo_config)
        log.info("with parametrization %s", self.space.configuration)

        return create_experiment(
            name=self.orion_config.name,
            version=self.orion_config.version,
            space=self.space,
            algorithms={algo_type: algo_config},
            strategy=None,
            max_trials=self.worker_config.max_trials,
            max_broken=self.worker_config.max_broken,
            storage=self.storage_config,
            branching=self.orion_config.branching,
            max_idle_time=None,
            heartbeat=None,
            working_dir=self.orion_config.workspace,
            debug=self.orion_config.debug,
            executor=None,
        )

    def sweep(self, arguments: List[str]) -> None:
        """Execute the optimization process"""

        assert self.config is not None
        assert self.launcher is not None
        assert self.job_idx is not None

        log.debug("Starting new experiment")
        self.client = self.new_experiment(arguments)

        with clientctx(self.client):
            try:
                self.optimize(self.client)
            except Exception as e:
                self.release_all()
                raise e

    def release_all(self) -> None:
        """Make sure not trials remain reserved"""
        for trial in self.pending_trials:
            try:
                self.client.release(trial, status="interrupted")
            except AlreadyReleased:
                pass

    def optimize(self, client: ExperimentClient) -> None:
        """Run the hyperparameter search in batches"""
        failures = []

        while not self.client.is_done:
            trials = self.sample_trials()

            returns = self.execute_trials(trials)

            self.observe_results(trials, returns, failures)

            if self.client.is_broken:
                if len(failures) == 0:
                    log.error(
                        "Experiment has reached is maximum amount of broken trials"
                    )
                    break

                # make the `Future` raise the exception it received
                try:
                    failures[-1].return_value
                except Exception as e:
                    raise BrokenExperiment("Max broken trials reached, stopping") from e

        self.show_results()

    def sample_trials(self) -> List[Trial]:
        """Sample a new batch of trials"""

        trials = self.suggest_trials(self.n_workers())
        log.debug("Suggest %d new trials", len(trials))
        self.pending_trials.update(set(trials))
        return trials

    def execute_trials(self, trials: List[Trial]) -> Sequence[JobReturn]:
        """Execture the given batch of trials"""

        overrides = list(as_overrides(t, self.arguments) for t in trials)
        self.validate_batch_is_legal(overrides)

        returns = self.launcher.launch(overrides, initial_job_idx=self.job_idx)
        self.job_idx += len(returns)
        return returns

    def observe_one(
        self, trial: Trial, result: JobReturn, failures: Sequence[JobReturn]
    ) -> None:
        """Observe a single trial"""
        value = result.return_value

        try:
            objective = to_objective(value)
            self.client.observe(trial, objective)

        except Exception as e:
            self.client.release(trial, status="broken")
            result.status = utils.JobStatus.FAILED
            result.return_value = e
            failures.append(result)

    def observe_results(
        self,
        trials: List[Trial],
        returns: Sequence[JobReturn],
        failures: Sequence[JobReturn],
    ):
        """Record the result of each trials"""
        for trial, result in zip(trials, returns):
            self.pending_trials.remove(trial)

            if result.status == utils.JobStatus.COMPLETED:
                self.observe_one(trial, result, failures)

            elif result.status == utils.JobStatus.FAILED:
                # We probably got an exception
                self.client.release(trial, status="broken")
                failures.append(result)

            elif result.status == utils.JobStatus.UNKNOWN:
                # Might be interrupted by user
                self.client.release(trial, status="interrupted")

    def show_results(self) -> None:
        """Retrieve the optimization stats and show which config was the best"""
        results = self.client.stats

        best_params = self.client.get_trial(uid=results.best_trials_id).params

        results = asdict(results)
        results["name"] = "orion"
        results["best_evaluated_params"] = best_params
        results["start_time"] = str(results["start_time"])
        results["finish_time"] = str(results["finish_time"])
        results["duration"] = str(results["duration"])

        OmegaConf.save(
            OmegaConf.create(results),
            f"{self.config.hydra.sweep.dir}/optimization_results.yaml",
        )

        log.info(
            "Best parameters: %s", " ".join(f"{x}={y}" for x, y in best_params.items())
        )
