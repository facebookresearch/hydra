# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import logging

from omegaconf import DictConfig, OmegaConf

import hydra
from hydra._internal.callback import Callback
from hydra.core.utils import JobReturn

log = logging.getLogger(__name__)


class CustomCallback(Callback):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
        self.name = self.__class__.__name__
        log.info(
            f"Init {self.name} with self.param1={self.param1}, self.param2={self.param2}"
        )

    def on_job_start(self, config: DictConfig, **kwargs) -> None:
        log.info(f"{self.name} on_job_start")

    def on_job_end(self, config: DictConfig, job_return: JobReturn, **kwargs) -> None:
        log.info(f"{self.name} on_job_end")

    def on_run_start(self, config: DictConfig, **kwargs) -> None:
        log.info(f"{self.name} on_run_start")

    def on_run_end(self, config: DictConfig, **kwargs) -> None:
        log.info(f"{self.name} on_run_end")

    def on_multirun_start(self, config: DictConfig, **kwargs) -> None:
        log.info(f"{self.name} on_multirun_start")

    def on_multirun_end(self, config: DictConfig, **kwargs) -> None:
        log.info(f"{self.name} on_multirun_end")


@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
