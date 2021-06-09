# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import logging
import os
import re
import sys
import warnings
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from os.path import splitext
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Dict, Optional, Sequence, Union, cast

from omegaconf import DictConfig, OmegaConf, open_dict, read_write

from hydra.core.hydra_config import HydraConfig
from hydra.core.singleton import Singleton
from hydra.types import HydraContext, TaskFunction

if TYPE_CHECKING:
    from hydra._internal.callbacks import Callbacks

log = logging.getLogger(__name__)


def simple_stdout_log_config(level: int = logging.INFO) -> None:
    root = logging.getLogger()
    root.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)


def configure_log(
    log_config: DictConfig,
    verbose_config: Union[bool, str, Sequence[str]] = False,
) -> None:
    assert isinstance(verbose_config, (bool, str)) or OmegaConf.is_list(verbose_config)
    if log_config is not None:
        conf: Dict[str, Any] = OmegaConf.to_container(  # type: ignore
            log_config, resolve=True
        )
        if conf["root"] is not None:
            logging.config.dictConfig(conf)
    else:
        # default logging to stdout
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s][%(name)s][%(levelname)s] - %(message)s"
        )
        handler.setFormatter(formatter)
        root.addHandler(handler)
    if isinstance(verbose_config, bool):
        if verbose_config:
            logging.getLogger().setLevel(logging.DEBUG)
    else:
        if isinstance(verbose_config, str):
            verbose_list = OmegaConf.create([verbose_config])
        elif OmegaConf.is_list(verbose_config):
            verbose_list = verbose_config  # type: ignore
        else:
            assert False

        for logger in verbose_list:
            logging.getLogger(logger).setLevel(logging.DEBUG)


def _save_config(cfg: DictConfig, filename: str, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(str(output_dir / filename), "w", encoding="utf-8") as file:
        file.write(OmegaConf.to_yaml(cfg))


def filter_overrides(overrides: Sequence[str]) -> Sequence[str]:
    """
    :param overrides: overrides list
    :return: returning a new overrides list with all the keys starting with hydra. filtered.
    """
    return [x for x in overrides if not x.startswith("hydra.")]


def _get_callbacks_for_run_job(hydra_context: Optional[HydraContext]) -> "Callbacks":
    if hydra_context is None:
        # DEPRECATED: remove in 1.2
        # hydra_context will be required in 1.2
        warnings.warn(
            message=dedent(
                """
                run_job's signature has changed in Hydra 1.1. Please pass in hydra_context.
                Support for the old style will be removed in Hydra 1.2.
                For more info, check https://github.com/facebookresearch/hydra/pull/1581."""
            ),
        )
        from hydra._internal.callbacks import Callbacks

        callbacks = Callbacks()
    else:
        callbacks = hydra_context.callbacks

    return callbacks


def run_job(
    task_function: TaskFunction,
    config: DictConfig,
    job_dir_key: str,
    job_subdir_key: Optional[str],
    configure_logging: bool = True,
    hydra_context: Optional[HydraContext] = None,
) -> "JobReturn":
    callbacks = _get_callbacks_for_run_job(hydra_context)

    old_cwd = os.getcwd()
    orig_hydra_cfg = HydraConfig.instance().cfg
    HydraConfig.instance().set_config(config)
    working_dir = str(OmegaConf.select(config, job_dir_key))
    if job_subdir_key is not None:
        # evaluate job_subdir_key lazily.
        # this is running on the client side in sweep and contains things such as job:id which
        # are only available there.
        subdir = str(OmegaConf.select(config, job_subdir_key))
        working_dir = os.path.join(working_dir, subdir)
    try:
        ret = JobReturn()
        ret.working_dir = working_dir
        task_cfg = copy.deepcopy(config)
        with read_write(task_cfg):
            with open_dict(task_cfg):
                del task_cfg["hydra"]

        ret.cfg = task_cfg
        hydra_cfg = copy.deepcopy(HydraConfig.instance().cfg)
        assert isinstance(hydra_cfg, DictConfig)
        ret.hydra_cfg = hydra_cfg
        overrides = OmegaConf.to_container(config.hydra.overrides.task)
        assert isinstance(overrides, list)
        ret.overrides = overrides
        # handle output directories here
        Path(str(working_dir)).mkdir(parents=True, exist_ok=True)
        os.chdir(working_dir)

        if configure_logging:
            configure_log(config.hydra.job_logging, config.hydra.verbose)

        if config.hydra.output_subdir is not None:
            hydra_output = Path(config.hydra.output_subdir)
            _save_config(task_cfg, "config.yaml", hydra_output)
            _save_config(hydra_cfg, "hydra.yaml", hydra_output)
            _save_config(config.hydra.overrides.task, "overrides.yaml", hydra_output)

        with env_override(hydra_cfg.hydra.job.env_set):
            callbacks.on_job_start(config=config)
            try:
                ret.return_value = task_function(task_cfg)
                ret.status = JobStatus.COMPLETED
            except Exception as e:
                ret.return_value = e
                ret.status = JobStatus.FAILED

        ret.task_name = JobRuntime.instance().get("name")

        _flush_loggers()

        callbacks.on_job_end(config=config, job_return=ret)

        return ret
    finally:
        HydraConfig.instance().cfg = orig_hydra_cfg
        os.chdir(old_cwd)


def get_valid_filename(s: str) -> str:
    s = str(s).strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "", s)


def setup_globals() -> None:
    # please add documentation when you add a new resolver
    OmegaConf.register_new_resolver(
        "now",
        lambda pattern: datetime.now().strftime(pattern),
        use_cache=True,
        replace=True,
    )
    OmegaConf.register_new_resolver(
        "hydra",
        lambda path: OmegaConf.select(cast(DictConfig, HydraConfig.get()), path),
        replace=True,
    )

    vi = sys.version_info
    version_dict = {
        "major": f"{vi[0]}",
        "minor": f"{vi[0]}.{vi[1]}",
        "micro": f"{vi[0]}.{vi[1]}.{vi[2]}",
    }
    OmegaConf.register_new_resolver(
        "python_version", lambda level="minor": version_dict.get(level), replace=True
    )


class JobStatus(Enum):
    UNKNOWN = 0
    COMPLETED = 1
    FAILED = 2


@dataclass
class JobReturn:
    overrides: Optional[Sequence[str]] = None
    cfg: Optional[DictConfig] = None
    hydra_cfg: Optional[DictConfig] = None
    working_dir: Optional[str] = None
    task_name: Optional[str] = None
    status: JobStatus = JobStatus.UNKNOWN
    _return_value: Any = None

    @property
    def return_value(self) -> Any:
        assert self.status != JobStatus.UNKNOWN, "return_value not yet available"
        if self.status == JobStatus.COMPLETED:
            return self._return_value
        else:
            sys.stderr.write(
                f"Error executing job with overrides: {self.overrides}" + os.linesep
            )
            raise self._return_value

    @return_value.setter
    def return_value(self, value: Any) -> None:
        self._return_value = value


class JobRuntime(metaclass=Singleton):
    def __init__(self) -> None:
        self.conf: DictConfig = OmegaConf.create()
        self.set("name", "UNKNOWN_NAME")

    def get(self, key: str) -> Any:
        ret = OmegaConf.select(self.conf, key)
        if ret is None:
            raise KeyError(f"Key not found in {type(self).__name__}: {key}")
        return ret

    def set(self, key: str, value: Any) -> None:
        log.debug(f"Setting {type(self).__name__}:{key}={value}")
        self.conf[key] = value


def validate_config_path(config_path: Optional[str]) -> None:
    if config_path is not None:
        split_file = splitext(config_path)
        if split_file[1] in (".yaml", ".yml"):
            msg = dedent(
                """\
            Using config_path to specify the config name is not supported, specify the config name via config_name.
            See https://hydra.cc/docs/next/upgrades/0.11_to_1.0/config_path_changes
            """
            )
            raise ValueError(msg)


@contextmanager
def env_override(env: Dict[str, str]) -> Any:
    """Temporarily set environment variables inside the context manager and
    fully restore previous environment afterwards
    """
    original_env = {key: os.getenv(key) for key in env}
    os.environ.update(env)
    try:
        yield
    finally:
        for key, value in original_env.items():
            if value is None:
                del os.environ[key]
            else:
                os.environ[key] = value


def _flush_loggers() -> None:
    # Python logging does not have an official API to flush all loggers.
    # This will have to do.
    for h_weak_ref in logging._handlerList:  # type: ignore
        try:
            h_weak_ref().flush()
        except Exception:
            # ignore exceptions thrown during flushing
            pass
