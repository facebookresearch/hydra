# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra
from hydra.core.hydra_config import HydraConfig


class MyCallable:
    def __init__(self, state: int = 123) -> None:
        self._state = state

    def __call__(self, cfg: DictConfig) -> None:
        print(self._state)
        print(HydraConfig.get().job.name)


my_callable = MyCallable()
my_app = hydra.main(version_base=None)(my_callable)

if __name__ == "__main__":
    my_app()
