import logging
import os
from functools import partial
from inspect import isclass
from pathlib import Path
from threading import Thread
from typing import Any, Dict, List, MutableMapping, MutableSequence, Optional, Union

import __main__
import wandb
import yaml
from hydra.core import plugins
from hydra.core.hydra_config import HydraConfig
from hydra.core.override_parser import overrides_parser
from hydra.core.override_parser.types import (
    ChoiceSweep,
    IntervalSweep,
    Override,
    RangeSweep,
    Transformer,
)
from hydra.core.utils import JobStatus
from hydra.plugins.sweeper import Sweeper
from hydra.types import HydraContext, TaskFunction
from hydra.utils import to_absolute_path
from omegaconf import DictConfig, ListConfig, OmegaConf
from wandb.agents.pyagent import Agent, RunStatus
from wandb.apis import InternalApi
from wandb.sdk.lib import filesystem
from wandb.sdk.wandb_setup import _EarlyLogger
from wandb.sdk.wandb_sweep import _get_sweep_url

from hydra_plugins.hydra_wandb_sweeper.config import WandbConfig, WandbParameterSpec

# TODO: switch to lazy %-style logging  (will make code look less readable though)
# https://docs.python.org/3/howto/logging.html#optimization
logger = logging.getLogger(__name__)

SUPPORTED_DISTRIBUTIONS = {
    "constant": ["value"],
    "categorical": ["values"],
    "int_uniform": ["min", "max"],
    "uniform": ["min", "max"],
    "q_uniform": ["min", "max", "q"],
    "log_uniform": ["min", "max"],
    "q_log_uniform": ["min", "max", "q"],
    "inv_log_uniform": ["min", "max"],
    "normal": ["mu", "sigma"],
    "q_normal": ["mu", "sigma", "q"],
    "log_normal": ["mu", "sigma"],
    "q_log_normal": ["mu", "sigma", "q"],
}

SUPPORTED_SEARCH_METHODS_AND_CONSTRAINTS = {
    "grid": ["value", "values"],
    "random": ["distribution"],
    "bayes": ["distribution"],
}

SUPPORTED_METRIC_ARGS = {
    "name": [str],
    "goal": ["minimize", "maximize"],
    "target": [float],
}

SUPPORTED_EARLY_TERM_ARGS = {
    "type": ["hyperband"],
    "min_iter": [int],
    "max_iter": [int],
    "s": [int],
    "eta": [int],
}


__original_cwd__ = os.getcwd()
__main_file__ = __main__.__file__


# Used by wandb.sweep since it checks if __stage_dir__ in wandb.old.core is set in
# order to create it for eventually saving the sweep config yaml to. If it's not set it defaults
# to 'wandb' + os.sep
wandb.old.core._set_stage_dir(".wandb" + os.sep)

"""
Wandb monkeypatches.
"""


def _my_gitrepo_init(self, root=None, remote="origin", lazy=True):
    self.remote_name = remote
    self._root = __original_cwd__ if root is None else root
    self._repo = None
    if not lazy:
        self.repo


# Monkeypatching GitRepo to use the original working directory as the root.
# This will allow wandb's code save features to be used properly when the hydra
# cwd is different than the code directory.
# Have to patch out here for submitit pickling purposes since out here is executed in the original working directory
# before the task function is pickled via executor.map_array. After unpickling at the node for task fn execution,
# the reference wandb.sdk.lib.git.GitRepo.__init__ -> _my_gitrepo_init is still preserved with original_cwd within
# _my_gitrepo_init preserving its previous value.
wandb.sdk.lib.git.GitRepo.__init__ = _my_gitrepo_init


def _my_save_config_file_from_dict(config_filename, config_dict):
    s = b"wandb_version: 1"
    if config_dict:  # adding an empty dictionary here causes a parse error
        s += b"\n\n" + yaml.dump(
            config_dict,
            Dumper=yaml.SafeDumper,
            default_flow_style=False,
            allow_unicode=True,
            encoding="utf-8",
        )
    data = s.decode("utf-8")
    if "/.wandb/" not in config_filename and "/wandb/" in config_filename:
        config_filename = config_filename.replace("/wandb/", "/.wandb/", 1)
        os.environ[wandb.env.SWEEP_PARAM_PATH] = config_filename
    filesystem._safe_makedirs(os.path.dirname(config_filename))
    with open(config_filename, "w") as conf_file:
        conf_file.write(data)


# Monkeypatching fn used by wandb.agent for creating the sweep config yaml file. It ignores __stage_dir__ which is
# where wandb.init stores its files (/path/to/.wandb/). Note that wandb.sweep uses a different __stage_dir__ which
# needed to be separately set above (very annoying).
# NOTE: This fn will eventually be moved in wandb.
wandb.sdk.lib.config_util.save_config_file_from_dict = _my_save_config_file_from_dict


def _my_get_program_relpath_from_gitrepo(
    program: str, _logger: Optional[_EarlyLogger] = None
) -> Optional[str]:
    repo = wandb.sdk.lib.git.GitRepo()
    root = repo.root
    if not root:
        root = os.getcwd()
    full_path_to_program = os.path.join(
        root, os.path.relpath(__original_cwd__, root), program
    )
    if os.path.exists(full_path_to_program):
        relative_path = os.path.relpath(full_path_to_program, start=root)
        if "../" in relative_path:
            if _logger:
                _logger.warning("could not save program above cwd: %s" % program)
            return None
        return relative_path

    if _logger:
        _logger.warning("could not find program at %s" % program)
    return None


# Monkeypatching to force wandb to use the original cwd when creating
# full_path_to_program. Otherwise the hydra cwd would be used, which could
# be located away from the code directory.
# Patching out here for same reasons explained in previous patch comment.
wandb.sdk.wandb_settings._get_program_relpath_from_gitrepo = (
    _my_get_program_relpath_from_gitrepo
)


"""
Sweeper helper functions.
"""


def is_wandb_override(override: Override) -> bool:
    if (
        override.is_delete()
        or override.is_add()
        or override.is_force_add()
        or override.is_hydra_override()
    ):
        return False
    else:
        return True


def get_parameter(distribution, *args) -> Dict[str, Any]:
    if distribution is not None:
        keys = SUPPORTED_DISTRIBUTIONS[distribution]
        parameter = {"distribution": distribution}
        for key, value in zip(keys, args):
            if value is None:
                raise TypeError(f"{key} must be assigned a value.")
            if distribution not in ("constant", "categorical"):
                if (key == "min" or key == "max") and "int" in distribution:
                    if not isinstance(value, int):
                        raise TypeError(
                            f"{value} assigned to {key} must be an integer."
                        )
                else:
                    value = float(value)
            if distribution in "constant" and isinstance(value, MutableSequence):
                assert len(value) == 1
                value = value[0]
            if isinstance(value, ListConfig):
                value = OmegaConf.to_container(value, resolve=True)
            parameter[key] = value
        return parameter
    else:
        parameter = {}
        for arg in args:
            if arg is None:
                raise TypeError("NoneType not accepted as a value.")
            if isinstance(arg, ListConfig):
                arg = OmegaConf.to_container(arg, resolve=True)
            if isinstance(arg, MutableSequence):
                assert len(arg) > 0
                if len(arg) == 1:
                    parameter["value"] = arg[0]
                if len(arg) > 1:
                    parameter["values"] = arg
                return parameter
            parameter["value"] = arg
            return parameter


def create_wandb_param_from_config(
    config: Union[MutableSequence[Any], MutableMapping[str, Any]], method: str
) -> Any:
    if isinstance(config, MutableSequence):
        if isinstance(config, ListConfig):
            config = OmegaConf.to_container(config, resolve=True)
        assert len(config) > 0
        if "distribution" in SUPPORTED_SEARCH_METHODS_AND_CONSTRAINTS[method]:
            distribution = "constant" if len(config) == 1 else "categorical"
        else:
            distribution = None
        return get_parameter(distribution, config)
    if isinstance(config, MutableMapping):
        specs = WandbParameterSpec(**config)
        if "distribution" in SUPPORTED_SEARCH_METHODS_AND_CONSTRAINTS[method]:
            distribution = specs.distribution
        else:
            distribution = None
        if distribution is not None:
            if distribution not in SUPPORTED_DISTRIBUTIONS:
                raise ValueError(
                    f"{distribution} not supported. "
                    f"Supported distributions: {list(SUPPORTED_DISTRIBUTIONS.keys())}"
                )
            supported_params = SUPPORTED_DISTRIBUTIONS[distribution]
            init_params = [getattr(specs, p) for p in supported_params]
        else:
            supported_params = SUPPORTED_SEARCH_METHODS_AND_CONSTRAINTS[method]
            init_params = [getattr(specs, p) for p in supported_params]
            if all(init_params):
                raise ValueError(
                    f"Only one of the supported constraint types must be provided: {supported_params}"
                )
            init_params = [param for param in init_params if param is not None]
        param = get_parameter(distribution, *init_params)
        return param
    if "distribution" in SUPPORTED_SEARCH_METHODS_AND_CONSTRAINTS[method]:
        param = get_parameter("constant", config)
    else:
        param = get_parameter(None, config)
    return param


def create_wandb_param_from_override(override: Override, method: str) -> Any:
    value = override.value()
    distribution = None
    if getattr(value, "tags", None):
        assert len(value.tags) == 1
        distribution = list(value.tags)[0]
        if distribution not in SUPPORTED_DISTRIBUTIONS:
            raise ValueError(
                f"{distribution} not supported. "
                f"Supported distributions: {list(SUPPORTED_DISTRIBUTIONS.keys())}"
            )
    if not override.is_sweep_override():
        if "distribution" in SUPPORTED_SEARCH_METHODS_AND_CONSTRAINTS[method]:
            param = get_parameter("constant", value)
        else:
            param = get_parameter(None, value)
        return param
    if override.is_interval_sweep():
        assert isinstance(value, IntervalSweep)
        distribution = distribution or "uniform"
        if "uniform" not in distribution or "q" in distribution:
            raise ValueError(
                f"Type IntervalSweep only supports non-quantized uniform distributions"
            )
        return get_parameter(distribution, value.start, value.end)
    if override.is_choice_sweep():
        assert isinstance(value, ChoiceSweep)
        choices = [x for x in override.sweep_iterator(transformer=Transformer.encode)]
        distribution = distribution or "categorical"
        if distribution != "categorical":
            raise ValueError(f"Type ChoiceSweep doesn't allow {distribution}")
        return get_parameter(distribution, choices)
    if override.is_range_sweep():
        assert isinstance(value, RangeSweep)
        distribution = distribution or "q_uniform"
        if "uniform" not in distribution or "q" not in distribution:
            raise ValueError(
                f"Type RangeSweep only supports quantized uniform distributions"
            )
        return get_parameter(distribution, value.start, value.end, value.step)

    raise NotImplementedError(f"{override} not supported by WandB sweeper")


def validate_metric(metric_dict):
    for key, val in metric_dict.items():
        if key not in SUPPORTED_METRIC_ARGS:
            raise KeyError(
                f"metric key {key} must be in supported keys: {list(SUPPORTED_METRIC_ARGS.keys())}."
            )
        supported = 0
        for supported_val in SUPPORTED_METRIC_ARGS[key]:
            if isclass(supported_val) and isinstance(val, supported_val):
                supported += 1
            elif not isclass(supported_val) and val == supported_val:
                supported += 1
        if supported == 0:
            raise ValueError(
                f"metric value {val} must be in supported types/values: {SUPPORTED_METRIC_ARGS[key]}."
            )


def validate_early_terminate(early_term_dict):
    if "min_iter" in early_term_dict and "max_iter" in early_term_dict:
        raise ValueError("Only either min_iter or max_iter must be provided, not both.")
    if "max_iter" in early_term_dict and not "s" in early_term_dict:
        raise KeyError("'s' is required when providing max_iter.")
    for key, val in early_term_dict.items():
        if key not in SUPPORTED_EARLY_TERM_ARGS:
            raise KeyError(
                f"early_terminate key {key} must be in supported keys: {list(SUPPORTED_EARLY_TERM_ARGS.keys())}."
            )
        supported = 0
        for supported_val in SUPPORTED_EARLY_TERM_ARGS[key]:
            if isclass(supported_val) and isinstance(val, supported_val):
                supported += 1
            elif not isclass(supported_val) and val == supported_val:
                supported += 1
        if supported == 0:
            raise ValueError(
                f"early_terminate value {val} must be in supported types/values: "
                f"{SUPPORTED_EARLY_TERM_ARGS[key]}."
            )


def validate_method_and_param_constraints(method, params_dict):
    if method not in SUPPORTED_SEARCH_METHODS_AND_CONSTRAINTS:
        raise ValueError(
            f"method {method} must be in supported search methods: "
            f"{list(SUPPORTED_SEARCH_METHODS_AND_CONSTRAINTS.keys())}."
        )
    constraints = SUPPORTED_SEARCH_METHODS_AND_CONSTRAINTS[method]
    for param_vals in params_dict.values():
        if not any(constraint in param_vals.keys() for constraint in constraints):
            raise ValueError(
                f"method {method} can only contain supported parameter constraints: "
                f"{constraints}. Offending param: {param_vals}"
            )


"""
Python helper functions.
"""


def _flatten_dict_gen(d, parent_key, sep):
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            yield from flatten_dict(v, new_key, sep=sep).items()
        else:
            yield new_key, v


def flatten_dict(d: MutableMapping, parent_key: str = "", sep: str = "."):
    return dict(_flatten_dict_gen(d, parent_key, sep))


# TODO: support for 'grid' sweep method. If user provides 'grid' as the search
# method, then we shouldn't be using SUPPORTED_DISTRIBUTIONS & "distribution"
# and instead return "value" or "values" if the user provides a single value
# or a list of values. This means we need to verify that "distribution" isn't
# provided by the user in any of the params to be sweeped through.
class WandbSweeperImpl(Sweeper):
    def __init__(
        self, wandb_sweep_config: WandbConfig, params: Optional[DictConfig]
    ) -> None:
        self.wandb_sweep_config = wandb_sweep_config
        self.params: Dict[str, Any] = {}

        # setup wandb params from hydra.sweep.params
        if params is not None:
            assert isinstance(params, DictConfig)
            self.params = {
                str(x): create_wandb_param_from_config(y, wandb_sweep_config.method)
                for x, y in params.items()
            }

        self.agent_run_count: Optional[int] = None
        self.job_idx: Optional[int] = None

        self.sweep_id = self.wandb_sweep_config.sweep_id
        self.wandb_tags = self.wandb_sweep_config.tags
        self.wandb_notes = self.wandb_sweep_config.notes

    def setup(
        self,
        *,
        hydra_context: HydraContext,
        task_function: TaskFunction,
        config: DictConfig,
    ) -> None:
        self.config = config
        self.agent_run_count = self.wandb_sweep_config.count
        self._task_function = self.WandbTask(
            wandb_sweeper=self, task_function=task_function
        )
        self.hydra_context = hydra_context
        self.job_idx = 0

        self.launcher = plugins.Plugins.instance().instantiate_launcher(
            config=config,
            hydra_context=hydra_context,
            task_function=self._task_function,
        )
        self.sweep_dict = {
            "name": self.wandb_sweep_config.name,
            "method": self.wandb_sweep_config.method,
            "parameters": self.params,
        }
        early_terminate = self.wandb_sweep_config.early_terminate
        metric = self.wandb_sweep_config.metric

        if metric:
            self.sweep_dict.update(
                {"metric": OmegaConf.to_container(metric, resolve=True)}
            )
            validate_metric(self.sweep_dict["metric"])

        if early_terminate:
            self.sweep_dict.update(
                {
                    "early_terminate": OmegaConf.to_container(
                        early_terminate, resolve=True
                    )
                }
            )
            validate_early_terminate(self.sweep_dict["early_terminate"])

        self.sweep_id = (
            OmegaConf.to_container(self.sweep_id, resolve=True)
            if self.sweep_id
            else None
        )
        self.wandb_tags = (
            OmegaConf.to_container(self.wandb_tags, resolve=True)
            if self.wandb_tags
            else None
        )
        self.wandb_notes = (
            str(OmegaConf.to_container(self.wandb_notes, resolve=True))
            if self.wandb_notes
            else None
        )

        # For keeping track of original code working directory without resorting to hydra.util get_original_cwd()
        # since HydraConfig hasn't been instantiated yet (happens after launch, which is too late)
        self.program = __main_file__
        self.program_relpath = __main_file__

    def sweep(self, arguments: List[str]) -> None:
        assert self.config is not None
        assert self.launcher is not None
        assert self.job_idx is not None

        parser = overrides_parser.OverridesParser.create()
        parsed = parser.parse_overrides(arguments)

        wandb_params = self.sweep_dict["parameters"]
        hydra_overrides = []

        # Separating command-line overrides meant for wandb params
        # from overrides meant for hydra configuration
        for override in parsed:
            if is_wandb_override(override):
                # Overriding wandb config params with wandb command line args
                wandb_params[
                    override.get_key_element()
                ] = create_wandb_param_from_override(
                    override, self.sweep_dict["method"]
                )
            else:
                hydra_overrides.append(override)

        validate_method_and_param_constraints(self.sweep_dict["method"], wandb_params)

        logger.info(
            f"WandbSweeper(method={self.wandb_sweep_config.method}, "
            f"num_agents={self.wandb_sweep_config.num_agents}, "
            f"count={self.wandb_sweep_config.count}, "
            f"budget={self.wandb_sweep_config.budget}, "
            f"entity={self.wandb_sweep_config.entity}, "
            f"project={self.wandb_sweep_config.project}, "
            f"name={self.wandb_sweep_config.name})"
        )
        logger.info(f"with parameterization {wandb_params}")
        logger.info(
            f"Sweep output dir: {to_absolute_path(self.config.hydra.sweep.dir)}"
        )

        # Creating this folder early so that wandb.init can write to this location.
        Path(to_absolute_path(self.config.hydra.sweep.dir)).mkdir(
            exist_ok=True, parents=True
        )
        (Path(to_absolute_path(self.config.hydra.sweep.dir)) / ".wandb").mkdir(
            exist_ok=True, parents=False
        )

        # Unfortuately wandb.sweep doesn't pay attn to this since it uses InternalApi which uses the old Settings
        # class that uses wandb.old.core for retrieving the wandb dir. It has its own __stage_dir__.
        os.environ["WANDB_DIR"] = to_absolute_path(self.config.hydra.sweep.dir)

        wandb_api = InternalApi()
        if not self.sweep_id:
            # Need to set PROGRAM env var to original program location since wandb.sweep can't take in a
            # wandb.Settings object, unlike wandb.init
            os.environ[wandb.env.PROGRAM] = self.program

            # Wandb sweep controller will only sweep through
            # params provided by self.sweep_dict
            self.sweep_id = wandb.sweep(
                self.sweep_dict,
                entity=self.wandb_sweep_config.entity,
                project=self.wandb_sweep_config.project,
            )
            logger.info(
                f"Starting Wandb Sweep with ID: {self.sweep_id} at URL: {_get_sweep_url(wandb_api, self.sweep_id)}"
            )
        else:
            logger.info(
                f"Reusing Wandb Sweep with ID: {self.sweep_id} at URL: {_get_sweep_url(wandb_api, self.sweep_id)}"
            )

        if not self.sweep_id:
            raise ValueError(
                f"Sweep with ID: {self.sweep_id} can not be created. "
                f"Either an invalid sweep_id was passed or the sweep does not exist."
            )

        remaining_budget = self.wandb_sweep_config.budget
        num_agents = self.wandb_sweep_config.num_agents
        all_returns: List[Any] = []
        while remaining_budget > 0:
            batch = min(num_agents, remaining_budget)
            remaining_budget -= batch

            # Repeating hydra overrides to match the number of wandb agents
            # requested. Each agent will interact with the wandb cloud controller
            # to receive hyperparams to send to its associated task function.
            overrides = []
            for _ in range(num_agents):
                overrides.append(
                    tuple(
                        f"{override.get_key_element()}={override.value()}"
                        for override in hydra_overrides
                    )
                )
            self.validate_batch_is_legal(overrides)

            # Hydra launcher will launch a wandb agent for each hydra override (which
            # will contain the base configuration to be overridden by wandb cloud controller)
            # It's recommended to set hydra.wandb_sweep_config.count to 1 if using the submitit
            # plugin -> https://docs.wandb.ai/guides/sweeps/faq#how-should-i-run-sweeps-on-slurm
            returns = self.launcher.launch(overrides, initial_job_idx=self.job_idx)
            self.job_idx += len(returns)

            # Check job status and wandb run statuses within each job
            job_failures = 0  # there can be a slim chance that the job fails before the agent is started
            num_unexpected_agent_errors = 0
            num_expected_agent_errors = 0
            unexpected_agent_errors = []
            expected_agent_errors = []
            num_runs = 0
            run_failures = 0
            failed_runs = []
            for ret in returns:
                if ret.status == JobStatus.COMPLETED:
                    for r in ret.return_value["run_results"]:
                        if r["status"] == JobStatus.FAILED:
                            run_failures += 1
                            failed_runs.append(r)
                    num_runs += sum(ret.return_value["num_runs"].values())

                    # Rare unexpected agent failures
                    if ret.return_value["agent_status"] == JobStatus.FAILED:
                        num_unexpected_agent_errors += 1
                        unexpected_agent_errors.append(ret.return_value["agent_error"])
                    elif (
                        ret.return_value["agent_status"] == JobStatus.COMPLETED
                        and ret.return_value["agent_status"] is not None
                    ):
                        num_expected_agent_errors += 1
                        # e.g., when a sweep was killed
                        expected_agent_errors.append(ret.return_value["agent_error"])
                else:
                    job_failures += 1

            # Raise if too many jobs in batch have failed (note that these are JobReturn objects)
            # Reuse max_agent_failure_rate. This is such a rare case so it's not worth exposing to the user for now.
            if (
                job_failures / len(returns)
                > self.wandb_sweep_config.max_agent_failure_rate
            ):
                logger.error(
                    f"{job_failures}/{len(returns)} Jobs failed "
                    f"with max_failure_rate={self.wandb_sweep_config.max_agent_failure_rate}. "
                    f"This is not an issue with the Agent but rather an issue elsewhere..."
                )
                for ret in returns:
                    ret.return_value  # delegate raising to JobReturn, with actual traceback

            # Raise if too many agents in batch have unexpectedly failed
            if (
                num_unexpected_agent_errors / len(returns)
                > self.wandb_sweep_config.max_agent_failure_rate
            ):
                logger.error(
                    f"{num_unexpected_agent_errors}/{len(returns)} Agents failed "
                    f"with max_failure_rate={self.wandb_sweep_config.max_agent_failure_rate}. "
                    f"This can possibly be caused by Sweep {self.sweep_id} not existing anymore."
                )
                # bundling agents' errors
                raise Exception(unexpected_agent_errors)

            # Raise if too many wandb run failures
            # NOTE: doesn't count runs from requeued agents (due to preemption) since they're run from a separate
            #       parent processs.
            if (
                num_runs > 0
                and run_failures / num_runs
                > self.wandb_sweep_config.max_run_failure_rate
            ):
                logger.error(
                    f"{run_failures}/{num_runs} Runs failed "
                    f"with max_failure_rate={self.wandb_sweep_config.max_run_failure_rate}"
                )
                # may as well include all failed runs in one bundled error
                raise Exception(failed_runs)

            if any(
                [
                    "Sweep has been killed." in e
                    for e in expected_agent_errors
                    if isinstance(e, str)
                ]
            ):
                logger.info(
                    f"Sweep {self.sweep_id} has been killed. Ending Hydra sweep."
                )
                break

            all_returns.extend(returns)

    class WandbTask(TaskFunction):
        """
        Inner class for exposing actual task_function and not the wandb wrapped one. This could be useful in cases
        such as when needing the launcher to be able to inspect the state of the inner task_function callable during
        checkpointing (in the case of using the submitit launcher plugin, for example).
        """

        def __init__(
            self, *, task_function: TaskFunction, wandb_sweeper: Sweeper
        ) -> None:
            self.inner_task_function = task_function
            self.wandb_sweeper = wandb_sweeper
            self.from_preemption = False
            self.agent_run_count = self.wandb_sweeper.agent_run_count
            self.max_num_agents = self.wandb_sweeper.wandb_sweep_config.budget
            self.max_num_runs = self.agent_run_count * self.max_num_agents
            self.num_runs = {}

        def __call__(self, base_config: DictConfig) -> None:
            runtime_cfg = HydraConfig.get()
            sweep_dir = Path(to_absolute_path(runtime_cfg.sweep.dir))
            sweep_subdir = sweep_dir / Path(runtime_cfg.sweep.subdir)

            # Need to set PROGRAM env var to original program location since passing it through wandb_settings doesn't
            # apply to wandb.agent which checks where the program is located in order to do code-save-related things.
            # However, with wandb.init we're fine since we pass wandb_settings to it.
            os.environ[wandb.env.PROGRAM] = self.wandb_sweeper.program
            wandb_settings = wandb.Settings(
                program=self.wandb_sweeper.program,
                program_relpath=self.wandb_sweeper.program_relpath,
                start_method="thread",
            )

            run_results: List[Any] = []

            def run(agent_id, run_status) -> Any:
                if self.from_preemption:
                    logger.info(
                        f"Agent {agent_id} initializing a Run after preemption..."
                    )
                else:
                    logger.info(f"Agent {agent_id} initializing a Run...")
                with wandb.init(
                    name=sweep_subdir.name,
                    group=sweep_dir.name,
                    settings=wandb_settings,
                    notes=self.wandb_sweeper.wandb_notes,
                    tags=self.wandb_sweeper.wandb_tags,
                    dir=str(sweep_dir),
                    resume=True if self.from_preemption else None,
                ) as run:
                    self.from_preemption = False
                    self.num_runs[agent_id] += 1

                    # Retrieving params from wandb sweep controller
                    override_dotlist = [
                        f"{dot}={val}" for dot, val in run.config.as_dict().items()
                    ]
                    override_config = OmegaConf.from_dotlist(override_dotlist)

                    # Merging base configuration with wandb sweep configs, overwriting base_config params with
                    # override_config params when there are matches (overwrite priority goes right-to-left)
                    config = OmegaConf.merge(base_config, override_config)

                    # Converting to Omegaconf, resolving, then converting from a nested dict to a flat dict
                    # with keys that are dot-delimited so that it matches the same dot-delimited param format that
                    # wandb's sweep controller received during creation
                    config_dict = OmegaConf.to_container(
                        config, resolve=True, throw_on_missing=True
                    )
                    config_dot_dict = flatten_dict(config_dict)

                    # Updating wandb run's param defaults with the dot-delimited params made above. The dict
                    # above includes params already set by wandb's sweep controller, so setdefaults won't overwrite
                    # those params and will only update params not configured by the sweep controller. This is so
                    # we can see all config params, including hydra params, in the wandb web interface.
                    run.config.setdefaults(config_dot_dict)

                    logger.info(
                        f"Agent {agent_id} initialized Run with ID: {run.id}, Name: {run.name}, "
                        f"Config: {flatten_dict(run.config.as_dict())} at URL: {run.get_url()}"
                    )

                    # TODO: catch RuntimeError('CUDA out of memory....) and tell wandb to mark the run as having
                    #       infinite loss so that it knows not to avoid those choice of params next time.
                    logger.info(
                        f"Agent {agent_id} executing task function under Run {run.id} ({run.name})..."
                    )
                    try:
                        ret = self.inner_task_function(config)
                        status = JobStatus.COMPLETED
                        run_results.append(
                            {
                                "run_id": run.id,
                                "name": run.name,
                                "return_value": ret,
                                "status": status,
                            }
                        )
                    except Exception as e:
                        if run_status[run.id] == RunStatus.STOPPED:
                            ret = "Run has been stopped by sweep controller"
                            status = JobStatus.COMPLETED
                        else:
                            ret = e
                            status = JobStatus.FAILED
                        run_results.append(
                            {
                                "run_id": run.id,
                                "name": run.name,
                                "return_value": ret,
                                "status": status,
                            }
                        )
                    # Catching any system exits from the task function so that we could inspect why the exit happened
                    # and pass a JobStatus and other useful info to the launcher pertaining to the exit. i.e.,
                    # don't stop everything just because a task function exited, just passively send the info to the
                    # launcher.
                    except SystemExit as e:
                        ret = e
                        if e.code == 0 or e.code is None:
                            status = JobStatus.COMPLETED
                        else:
                            status = JobStatus.FAILED
                        run_results.append(
                            {
                                "run_id": run.id,
                                "name": run.name,
                                "return_value": ret,
                                "status": status,
                            }
                        )
                    finally:
                        if isinstance(ret, BaseException):
                            ret = repr(ret)
                        logger.info(
                            f"Agent finished executing task function under Run {run.id} ({run.name}) "
                            f"with status: {status} and return value: {ret}"
                        )

            def agent_run(agent):
                agent._heartbeat_thread = Thread(target=agent._heartbeat)
                agent._heartbeat_thread.daemon = True
                agent._heartbeat_thread.start()
                agent._run_jobs_from_queue()

            try:
                agent_status = JobStatus.COMPLETED
                agent_error = None
                num_runs_so_far = sum(self.num_runs.values())
                if num_runs_so_far <= self.max_num_runs:
                    agent = Agent(
                        self.wandb_sweeper.sweep_id, count=self.agent_run_count
                    )
                    try:
                        agent._setup()
                    except Exception as e:
                        agent_id = None
                        agent_error = "Sweep has been killed."
                        agent_status = JobStatus.COMPLETED
                    else:
                        agent_id = str(agent._agent_id)
                        self.num_runs[agent_id] = 0
                        agent._function = partial(run, agent_id, agent._run_status)
                        logger.info(f"Launching a Wandb Agent with ID: {agent_id}...")
                        agent_run(agent)  # <--- main task function loop
            # Catch unexpected exceptions pertaining to the agent execution and give a FAILED
            # JobStatus. Expected exceptions, on the other hand, include sweep being killed,
            # runs being stopped, etc. and give a COMPLETED JobStatus.
            except Exception as e:
                agent_status = JobStatus.FAILED
                agent_error = e
            # Catching system exits that are performed on the outer task function
            # (i.e., this function, __call__). This can potentially come from the checkpoint
            # function in the submitit launcher.
            except SystemExit as e:
                agent_error = e
                if e.code == 0 or e.code is None or e.code == -1:
                    agent_status = JobStatus.COMPLETED
                else:
                    agent_status = JobStatus.FAILED
            finally:
                return {
                    "agent_id": agent_id,
                    "run_results": run_results,
                    "agent_status": agent_status,
                    "agent_error": agent_error,
                    "num_runs": self.num_runs,
                }
