# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import logging
import os
import re
import sys
import warnings
from contextlib import contextmanager
from dataclasses import dataclass
from os.path import basename, dirname, splitext
from pathlib import Path
from time import localtime, strftime
from typing import Any, Dict, Optional, Sequence, Tuple, Union, cast

from omegaconf import DictConfig, OmegaConf
from omegaconf import __version__ as oc_version
from omegaconf import open_dict, read_write

from hydra.core.hydra_config import HydraConfig
from hydra.core.singleton import Singleton
from hydra.types import TaskFunction

log = logging.getLogger(__name__)


def simple_stdout_log_config(level: int = logging.INFO) -> None:
    root = logging.getLogger()
    root.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)


def configure_log(
    log_config: DictConfig, verbose_config: Union[bool, str, Sequence[str]]
) -> None:
    assert isinstance(verbose_config, (bool, str)) or OmegaConf.is_list(verbose_config)
    if log_config is not None:
        conf: Dict[str, Any] = OmegaConf.to_container(  # type: ignore
            log_config, resolve=True
        )
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
    with open(str(output_dir / filename), "w") as file:
        file.write(OmegaConf.to_yaml(cfg))


def filter_overrides(overrides: Sequence[str]) -> Sequence[str]:
    """
    :param overrides: overrides list
    :return: returning a new overrides list with all the keys starting with hydra. filtered.
    """
    return [x for x in overrides if not x.startswith("hydra.")]


def run_job(
    config: DictConfig,
    task_function: TaskFunction,
    job_dir_key: str,
    job_subdir_key: Optional[str],
    configure_logging: bool = True,
) -> "JobReturn":
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
            ret.return_value = task_function(task_cfg)
        ret.task_name = JobRuntime.instance().get("name")

        _flush_loggers()

        return ret
    finally:
        HydraConfig.instance().cfg = orig_hydra_cfg
        os.chdir(old_cwd)


def get_valid_filename(s: str) -> str:
    s = str(s).strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "", s)


def setup_globals() -> None:
    oc_major_ver = tuple(int(x) for x in oc_version.split(".")[0:2])

    def register(name: str, f: Any, cache: bool = False) -> None:
        if oc_major_ver >= (2, 1):
            OmegaConf.register_new_resolver(name, f, replace=True, use_cache=cache)  # type: ignore
        else:
            try:
                OmegaConf.register_resolver(name, f)
            except AssertionError:
                # calling it again in no_workers mode will throw. safe to ignore.
                pass

    # please add documentation when you add a new resolver
    register("now", lambda pattern: strftime(pattern, localtime()), cache=True)
    register(
        "hydra",
        lambda path: OmegaConf.select(cast(DictConfig, HydraConfig.get()), path),
    )

    vi = sys.version_info
    version_dict = {
        "major": f"{vi[0]}",
        "minor": f"{vi[0]}.{vi[1]}",
        "micro": f"{vi[0]}.{vi[1]}.{vi[2]}",
    }
    register("python_version", lambda level="minor": version_dict.get(level))


@dataclass
class JobReturn:
    overrides: Optional[Sequence[str]] = None
    return_value: Any = None
    cfg: Optional[DictConfig] = None
    hydra_cfg: Optional[DictConfig] = None
    working_dir: Optional[str] = None
    task_name: Optional[str] = None


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


def split_config_path(
    config_path: Optional[str], config_name: Optional[str]
) -> Tuple[Optional[str], Optional[str]]:
    if config_path is None or config_path == "":
        return None, config_name
    split_file = splitext(config_path)
    if split_file[1] in (".yaml", ".yml"):
        # assuming dir/config.yaml form
        config_file: Optional[str] = basename(config_path)
        config_dir: Optional[str] = dirname(config_path)
        msg = (
            "\nUsing config_path to specify the config name is deprecated, specify the config name via config_name"
            "\nSee https://hydra.cc/docs/next/upgrades/0.11_to_1.0/config_path_changes"
        )
        warnings.warn(category=UserWarning, message=msg)
    else:
        # assuming dir form without a config file.
        config_file = None
        config_dir = config_path

    if config_dir == "":
        config_dir = None

    if config_file == "":
        config_file = None

    if config_file is not None:
        if config_name is not None:
            raise ValueError(
                "Config name should be specified in either normalized_config_path or config_name, but not both"
            )
        config_name = config_file

    return config_dir, config_name


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
