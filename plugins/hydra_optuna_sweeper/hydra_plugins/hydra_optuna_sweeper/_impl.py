# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import sys
import pickle
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Dict, List, MutableMapping, MutableSequence, Optional

from joblib import Parallel, delayed
import optuna
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
from hydra.types import HydraContext, TaskFunction
from hydra.utils import instantiate
from omegaconf import DictConfig, OmegaConf
from optuna.distributions import (
    BaseDistribution,
    CategoricalChoiceType,
    CategoricalDistribution,
    DiscreteUniformDistribution,
    IntLogUniformDistribution,
    IntUniformDistribution,
    LogUniformDistribution,
    UniformDistribution,
)

from .config import Direction, DistributionConfig, DistributionType

log = logging.getLogger(__name__)


def create_optuna_distribution_from_config(
    config: MutableMapping[str, Any]
) -> BaseDistribution:
    kwargs = dict(config)
    if isinstance(config["type"], str):
        kwargs["type"] = DistributionType[config["type"]]
    param = DistributionConfig(**kwargs)
    if param.type == DistributionType.categorical:
        assert param.choices is not None
        return CategoricalDistribution(param.choices)
    if param.type == DistributionType.int:
        assert param.low is not None
        assert param.high is not None
        if param.log:
            return IntLogUniformDistribution(int(param.low), int(param.high))
        step = int(param.step) if param.step is not None else 1
        return IntUniformDistribution(int(param.low), int(param.high), step=step)
    if param.type == DistributionType.float:
        assert param.low is not None
        assert param.high is not None
        if param.log:
            return LogUniformDistribution(param.low, param.high)
        if param.step is not None:
            return DiscreteUniformDistribution(param.low, param.high, param.step)
        return UniformDistribution(param.low, param.high)
    raise NotImplementedError(f"{param.type} is not supported by Optuna sweeper.")


def create_optuna_distribution_from_override(override: Override) -> Any:
    if not override.is_sweep_override():
        return override.get_value_element_as_str()

    value = override.value()
    choices: List[CategoricalChoiceType] = []
    if override.is_choice_sweep():
        assert isinstance(value, ChoiceSweep)
        for x in override.sweep_iterator(transformer=Transformer.encode):
            assert isinstance(
                x, (str, int, float, bool)
            ), f"A choice sweep expects str, int, float, or bool type. Got {type(x)}."
            choices.append(x)
        return CategoricalDistribution(choices)

    if override.is_range_sweep():
        assert isinstance(value, RangeSweep)
        assert value.start is not None
        assert value.stop is not None
        if value.shuffle:
            for x in override.sweep_iterator(transformer=Transformer.encode):
                assert isinstance(
                    x, (str, int, float, bool)
                ), f"A choice sweep expects str, int, float, or bool type. Got {type(x)}."
                choices.append(x)
            return CategoricalDistribution(choices)
        return IntUniformDistribution(
            int(value.start), int(value.stop), step=int(value.step)
        )

    if override.is_interval_sweep():
        assert isinstance(value, IntervalSweep)
        assert value.start is not None
        assert value.end is not None
        if "log" in value.tags:
            if isinstance(value.start, int) and isinstance(value.end, int):
                return IntLogUniformDistribution(int(value.start), int(value.end))
            return LogUniformDistribution(value.start, value.end)
        else:
            if isinstance(value.start, int) and isinstance(value.end, int):
                return IntUniformDistribution(value.start, value.end)
            return UniformDistribution(value.start, value.end)

    raise NotImplementedError(f"{override} is not supported by Optuna sweeper.")

def create_optuna_trial_override(trial, dir: str):
    with NamedTemporaryFile(delete=False, dir=dir, prefix='optuna_trial_') as f:
        pickle.dump(trial, f)
        fname = f.name

    return {'+trial': '{'
        '_target_:pickle.load,'
        'file:{'
            '_target_:io.open,'
            'mode:rb,'
            f'file:{fname}'
        '}}'
    }

class OptunaSweeperImpl(Sweeper):
    def __init__(
        self,
        sampler: Any,
        direction: Any,
        storage: Optional[str],
        study_name: Optional[str],
        n_trials: int,
        n_jobs: int,
        search_space: Optional[DictConfig],
        pruner: Optional[Any],
    ) -> None:
        self.sampler = sampler
        self.direction = direction
        self.storage = storage
        self.study_name = study_name
        self.n_trials = n_trials
        self.n_jobs = n_jobs
        self.pruner = pruner if pruner is not None else optuna.pruners.NopPruner()
        self.search_space = {}
        if search_space:
            assert isinstance(search_space, DictConfig)
            self.search_space = {
                str(x): create_optuna_distribution_from_config(y)
                for x, y in search_space.items()
            }
        self.job_idx: int = 0

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
        self.launcher = Plugins.instance().instantiate_launcher(
            config=config, hydra_context=hydra_context, task_function=task_function
        )

        sweep_dir = Path(config.hydra.sweep.dir).absolute()
        sweep_dir.mkdir(parents=True, exist_ok=True)
        self.sweep_dir = str(sweep_dir)

    def sweep(self, arguments: List[str]) -> None:
        assert self.config is not None
        assert self.launcher is not None
        assert self.hydra_context is not None
        assert self.job_idx is not None

        parser = OverridesParser.create()
        parsed = parser.parse_overrides(arguments)

        search_space = dict(self.search_space)
        fixed_params = dict()
        for override in parsed:
            value = create_optuna_distribution_from_override(override)
            if isinstance(value, BaseDistribution):
                search_space[override.get_key_element()] = value
            else:
                fixed_params[override.get_key_element()] = value
        
        # Remove fixed parameters from Optuna search space.
        for param_name in fixed_params:
            if param_name in search_space:
                del search_space[param_name]

        directions: List[str] = ([
            d.name if isinstance(d, Direction) else d for d in (
                self.direction if isinstance(self.direction, MutableSequence) else [self.direction]
            )
        ])

        study = optuna.create_study(
            study_name=self.study_name,
            storage=self.storage,
            sampler=self.sampler,
            directions=directions,
            load_if_exists=True,
            pruner=self.pruner
        )

        log.info(f"Study name: {study.study_name}")
        log.info(f"Storage: {self.storage}")
        log.info(f"Sampler: {type(self.sampler).__name__}")
        log.info(f"Directions: {directions}")

        Parallel(n_jobs=self.n_jobs, prefer='threads', require='sharedmem')(
            delayed(self.__run_trial)(
                study=study,
                search_space=search_space,
                fixed_params=fixed_params,
                directions=directions,
                job_id=i
            ) for i in range(self.n_trials)
        )

        results_to_serialize: Dict[str, Any]
        if len(directions) < 2:
            best_trial = study.best_trial
            results_to_serialize = {
                "name": "optuna",
                "best_params": best_trial.params,
                "best_value": best_trial.value,
            }
            log.info(f"Best parameters: {best_trial.params}")
            log.info(f"Best value: {best_trial.value}")
        else:
            best_trials = study.best_trials
            pareto_front = [
                {"params": t.params, "values": t.values} for t in best_trials
            ]
            results_to_serialize = {
                "name": "optuna",
                "solutions": pareto_front,
            }
            log.info(f"Number of Pareto solutions: {len(best_trials)}")
            for t in best_trials:
                log.info(f"    Values: {t.values}, Params: {t.params}")
        OmegaConf.save(
            OmegaConf.create(results_to_serialize),
            f"{self.config.hydra.sweep.dir}/optimization_results.yaml",
        )

    def __run_trial(self, study, search_space, fixed_params, directions, job_id):
        self.job_idx += 1

        trial = study.ask()
        overrides = []
        for param_name, distribution in search_space.items():
            trial._suggest(param_name, distribution)

        params = dict(trial.params)
        params.update(fixed_params)
        params.update(create_optuna_trial_override(trial, dir=self.sweep_dir))
            
        overrides.append(tuple(f"{name}={val}" for name, val in params.items()))

        returns = self.launcher.launch(overrides, initial_job_idx=job_id)

        values: Optional[List[float]] = None
        state: optuna.trial.TrialState = optuna.trial.TrialState.COMPLETE

        try:
            try:
                values = [float(v) for v in (
                    [returns.return_value] if len(directions) == 1 else returns.return_value
                )]
            except (ValueError, TypeError):
                raise ValueError(
                    "Return value(s) must be float-castable,"
                    " and a sequence if multiple objectives are used."
                    f" Got '{returns.return_value}'."
                ).with_traceback(sys.exc_info()[2])

            if len(values) != len(directions):
                raise ValueError(
                    "The number of the values and the number of the objectives are"
                    f" mismatched. Expect {len(directions)}, but actually {len(values)}."
                )
        except optuna.exceptions.TrialPruned:
            state = optuna.trial.TrialState.PRUNED
        except Exception as e:
            state = optuna.trial.TrialState.FAIL
        finally:
            study.tell(trial=trial, state=state, values=values)