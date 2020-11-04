import logging

from omegaconf import DictConfig

from hydra.callbacks.callbacks import Callbacks

log = logging.getLogger(__name__)


class ExampleCallbacks(Callbacks):
    def pre_run(self, cfg: DictConfig) -> None:
        log.info("ExampleCallbacks pre_run called")

    def post_run(self, cfg: DictConfig) -> None:
        log.info("ExampleCallbacks post_run called")

    def pre_sweep(self, sweep_cfg: DictConfig) -> None:
        log.info("ExampleCallbacks pre_sweep called")

    def post_sweep(self, sweep_cfg: DictConfig) -> None:
        log.info("ExampleCallbacks post_sweep called")

    def pre_job(self, job_cfg: DictConfig) -> None:
        log.info("ExampleCallbacks pre_job called")

    def post_job(self, job_cfg: DictConfig) -> None:
        log.info("ExampleCallbacks post_job called")
