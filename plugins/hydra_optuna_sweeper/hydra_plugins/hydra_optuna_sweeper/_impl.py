# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
from typing import Any, List, MutableMapping, Optional

import optuna
from hydra.core.config_loader import ConfigLoader
from hydra.core.override_parser.overrides_parser import OverridesParser
from hydra.core.override_parser.types import (
    ChoiceSweep,
    IntervalSweep,
    Override,
    RangeSweep,
    Transformer,
)
from hydra.core.plugins import Plugins
from hydra.plugins.sweeper import Sweeper
from hydra.types import TaskFunction
from omegaconf import DictConfig, OmegaConf
from optuna.distributions import (
    CategoricalDistribution,
    DiscreteUniformDistribution,
    IntLogUniformDistribution,
    IntUniformDistribution,
    LogUniformDistribution,
    UniformDistribution,
)
from optuna.samplers import CmaEsSampler, RandomSampler, TPESampler

from .config import DistributionConfig, OptunaConfig

log = logging.getLogger(__name__)


def create_optuna_distribution_from_config(config: MutableMapping[str, Any]) -> Any:
    param = DistributionConfig(**config)
    if param.type == "categorical":
        assert param.choices is not None
        return CategoricalDistribution(param.choices)
    if param.type == "int":
        assert param.low is not None
        assert param.high is not None
        if param.log:
            return IntLogUniformDistribution(int(param.low), int(param.high))
        return IntUniformDistribution(
            int(param.low), int(param.high), step=int(param.step)
        )
    if param.type == "float":
        assert param.low is not None
        assert param.high is not None
        if param.log:
            return LogUniformDistribution(param.low, param.high)
        if param.step != 1:
            return DiscreteUniformDistribution(param.low, param.high, param.step)
        return UniformDistribution(param.low, param.high)
    return config


def create_optuna_distribution_from_override(override: Override) -> Any:
    value = override.value()
    if not override.is_sweep_override():
        return value

    if override.is_choice_sweep():
        assert isinstance(value, ChoiceSweep)
        choices = [x for x in override.sweep_iterator(transformer=Transformer.encode)]
        _choices = [x for x in choices if isinstance(x, (str, int, float))]
        assert choices == _choices
        return CategoricalDistribution(_choices)

    if override.is_range_sweep():
        assert isinstance(value, RangeSweep)
        assert value.start is not None
        assert value.stop is not None
        if value.shuffle:
            choices = [
                x for x in override.sweep_iterator(transformer=Transformer.encode)
            ]
            _choices = [x for x in choices if isinstance(x, (str, int, float))]
            assert choices == _choices
            return CategoricalDistribution(_choices)
        return IntUniformDistribution(
            int(value.start), int(value.stop), step=int(value.step)
        )

    if override.is_interval_sweep():
        assert isinstance(value, IntervalSweep)
        assert value.start is not None
        assert value.end is not None
        if "log" in value.tags:
            if "int" in value.tags:
                return IntLogUniformDistribution(int(value.start), int(value.end))
            return LogUniformDistribution(value.start, value.end)
        else:
            if "int" in value.tags:
                return IntUniformDistribution(int(value.start), int(value.end))
            return UniformDistribution(value.start, value.end)

    raise NotImplementedError("{} is not supported by Optuna sweeper.".format(override))


class OptunaSweeperImpl(Sweeper):
    def __init__(
        self, optuna_config: OptunaConfig, search_space: Optional[DictConfig]
    ) -> None:
        self.optuna_config = optuna_config
        self.search_space = {}
        if search_space:
            assert isinstance(search_space, DictConfig)
            self.search_space = {
                x: create_optuna_distribution_from_config(y)
                for x, y in search_space.items()
            }

    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:

        self.config = config
        self.config_loader = config_loader
        self.launcher = Plugins.instance().instantiate_launcher(
            config=config, config_loader=config_loader, task_function=task_function
        )
        self.sweep_dir = config.hydra.sweep.dir

    def sweep(self, arguments: List[str]) -> None:
        assert self.config is not None
        assert self.launcher is not None

        parser = OverridesParser.create()
        parsed = parser.parse_overrides(arguments)

        search_space = dict(self.search_space)
        for override in parsed:
            search_space[
                override.get_key_element()
            ] = create_optuna_distribution_from_override(override)

        if self.optuna_config.sampler:
            sampler_class = getattr(optuna.samplers, self.optuna_config.sampler)
        else:
            sampler_class = TPESampler

        if sampler_class in {CmaEsSampler, RandomSampler, TPESampler}:
            sampler = sampler_class(seed=self.optuna_config.seed)
        else:
            sampler = sampler_class()

        study = optuna.create_study(
            study_name=self.optuna_config.study_name,
            storage=self.optuna_config.storage,
            sampler=sampler,
            direction=self.optuna_config.direction.name,
        )
        log.info(f"Study name: {self.optuna_config.study_name}")
        log.info(f"Storage: {self.optuna_config.storage}")
        log.info(f"Sampler: {self.optuna_config.sampler}")
        log.info(f"Direction: {self.optuna_config.direction}")

        batch_size = self.optuna_config.n_jobs
        n_trials_to_go = self.optuna_config.n_trials

        while n_trials_to_go > 0:
            batch_size = min(n_trials_to_go, batch_size)

            trials = [study._ask() for _ in range(batch_size)]
            overrides = []
            for trial in trials:
                for param_name, distribution in search_space.items():
                    trial._suggest(param_name, distribution)
                
                overrides.append(
                    tuple(f"{name}={val}" for name, val in trial.params.items())
                )

            returns = self.launcher.launch(overrides, initial_job_idx=trials[0].number)
            for trial, ret in zip(trials, returns):
                study._tell(trial, optuna.trial.TrialState.COMPLETE, ret.return_value)
            n_trials_to_go -= batch_size

        best_trial = study.best_trial
        results_to_serialize = {
            "name": "optuna",
            "best_params": best_trial.params,
            "best_value": best_trial.value,
        }
        OmegaConf.save(
            OmegaConf.create(results_to_serialize),
            f"{self.config.hydra.sweep.dir}/optimization_results.yaml",
        )
        log.info(f"Best parameters: {best_trial.params}")
        log.info(f"Best value: {best_trial.value}")
