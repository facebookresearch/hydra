# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging

from omegaconf import DictConfig, OmegaConf

import hydra
from hydra.core.utils import JobReturn
from hydra.experimental.callback import Callback

log = logging.getLogger(__name__)


class DefaultCallback(Callback):
    def __init__(self):
        self.name = self.__class__.__name__

    def on_job_start(self, config: DictConfig, **kwargs) -> None:
        log.info(f"{self.name} on_job_start")

    def on_job_end(self, config: DictConfig, job_return: JobReturn, **kwargs) -> None:
        log.info(f"{self.name} on_job_end")


@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
