import logging
import os

from .config_loader import ConfigLoader
from .plugins import Plugins
from .utils import (
    get_valid_filename,
    JobRuntime,
    HydraConfig,
    setup_globals,
    run_job,
    configure_log,
)

log = None


class Hydra:
    def __init__(
        self, task_name, conf_dir, conf_filename, task_function, verbose, strict
    ):
        setup_globals()
        JobRuntime().set("name", get_valid_filename(task_name))
        self.task_name = task_name
        self.conf_dir = conf_dir
        self.conf_filename = conf_filename
        self.task_function = task_function
        if not os.path.exists(self.conf_dir):
            raise IOError("Config directory '{}' not found".format(self.conf_dir))
        if self.conf_filename is not None:
            if not os.path.exists(os.path.join(self.conf_dir, self.conf_filename)):
                raise IOError("Config directory '{}' not found".format(self.conf_dir))
        self.config_loader = ConfigLoader(
            conf_filename=self.conf_filename,
            conf_dir=self.conf_dir,
            strict_cfg=strict,
            config_path=[
                "pkg://hydra.default_conf",
                os.path.join(self.conf_dir, ".hydra"),
            ],
        )
        self.verbose = verbose

    def run(self, overrides):
        cfg = self._load_config(overrides)
        HydraConfig().set_config(cfg)
        return run_job(
            config=cfg,
            task_function=self.task_function,
            verbose=self.verbose,
            job_dir_key="hydra.run.dir",
            job_subdir_key=None,
        )

    def multirun(self, overrides):
        cfg = self._load_config(overrides)
        HydraConfig().set_config(cfg)
        sweeper = Plugins.instantiate_sweeper(
            config=cfg,
            config_loader=self.config_loader,
            task_function=self.task_function,
            verbose=self.verbose,
        )
        return sweeper.sweep(arguments=cfg.hydra.overrides.task)

    def show_cfg(self, overrides):
        config = self._load_config(overrides)
        log.info("\n" + config.pretty())

    def _load_config(self, overrides):
        cfg = self.config_loader.load_configuration(overrides)
        configure_log(cfg.hydra.hydra_logging, self.verbose)
        global log
        log = logging.getLogger(__name__)
        _print_load_history(self.config_loader)
        return cfg


def _print_load_history(loader):
    for file, loaded in loader.get_load_history():
        if loaded:
            log.debug("Loaded: {}".format(file))
        else:
            log.debug("Not found: {}".format(file))
