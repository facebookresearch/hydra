# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import logging
import os
import re
import sys
from dataclasses import dataclass
from os.path import basename, dirname, splitext
from pathlib import Path
from time import localtime, strftime
from typing import Any, Dict, Optional, Sequence, Tuple, Union

from omegaconf import DictConfig, OmegaConf

from hydra.core.hydra_config import HydraConfig
from hydra.core.singleton import Singleton
from hydra.types import TaskFunction

log = logging.getLogger(__name__)


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
        file.write(cfg.pretty())


def get_overrides_dirname(
    input_list: Sequence[str],
    exclude_keys: Sequence[str] = [],
    item_sep: str = ",",
    kv_sep: str = "=",
) -> str:
    lst = []
    for x in input_list:
        key, _val = split_key_val(x)
        if key not in exclude_keys:
            lst.append(x)

    lst.sort()
    ret = re.sub(pattern="[=]", repl=kv_sep, string=item_sep.join(lst))
    return ret


def filter_overrides(overrides: Sequence[str]) -> Sequence[str]:
    """
    :param overrides: overrides list
    :return: returning a new overrides list with all the keys starting with hydra. filtered.
    """
    return [x for x in overrides if not x.startswith("hydra.")]


def split_key_val(s: str) -> Tuple[str, str]:
    assert "=" in s, "'{}' not a valid override, expecting key=value format".format(s)

    idx = s.find("=")
    assert idx != -1
    return s[0:idx], s[idx + 1 :]


def run_job(
    config: DictConfig,
    task_function: TaskFunction,
    job_dir_key: str,
    job_subdir_key: Optional[str],
) -> "JobReturn":
    old_cwd = os.getcwd()
    working_dir = str(config.select(job_dir_key))
    if job_subdir_key is not None:
        # evaluate job_subdir_key lazily.
        # this is running on the client side in sweep and contains things such as job:id which
        # are only available there.
        subdir = str(config.select(job_subdir_key))
        working_dir = os.path.join(working_dir, subdir)
    try:
        ret = JobReturn()
        ret.working_dir = working_dir
        task_cfg = copy.deepcopy(config)
        del task_cfg["hydra"]
        ret.cfg = task_cfg
        ret.hydra_cfg = OmegaConf.create({"hydra": HydraConfig.instance().hydra})
        overrides = OmegaConf.to_container(config.hydra.overrides.task)
        assert isinstance(overrides, list)
        ret.overrides = overrides
        # handle output directories here
        Path(str(working_dir)).mkdir(parents=True, exist_ok=True)
        os.chdir(working_dir)
        hydra_output = Path(config.hydra.output_subdir)

        configure_log(config.hydra.job_logging, config.hydra.verbose)

        hydra_cfg = OmegaConf.masked_copy(config, "hydra")
        assert isinstance(hydra_cfg, DictConfig)

        _save_config(task_cfg, "config.yaml", hydra_output)
        _save_config(hydra_cfg, "hydra.yaml", hydra_output)
        _save_config(config.hydra.overrides.task, "overrides.yaml", hydra_output)
        ret.return_value = task_function(task_cfg)
        ret.task_name = JobRuntime.instance().get("name")

        # shut down logging to ensure job log files are closed.
        # If logging is still required after run_job caller is responsible to re-initialize it.
        logging.shutdown()

        return ret
    finally:
        os.chdir(old_cwd)


def get_valid_filename(s: str) -> str:
    s = str(s).strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "", s)


def setup_globals() -> None:
    try:
        OmegaConf.register_resolver(
            "now", lambda pattern: strftime(pattern, localtime())
        )
    except AssertionError:
        # calling it again in no_workers mode will throw. safe to ignore.
        pass


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
        ret = self.conf.select(key)
        if ret is None:
            raise KeyError("Key not found in {}: {}".format(type(self).__name__, key))
        return ret

    def set(self, key: str, value: Any) -> None:
        log.debug("Setting {}:{}={}".format(type(self).__name__, key, value))
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
                "Config name should be specified in either config_path or config_name, but not both"
            )
        config_name = config_file

    return config_dir, config_name
