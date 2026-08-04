# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore


@dataclass(frozen=True)
class SerialPort:
    baud_rate: int = 19200
    data_bits: int = 8
    stop_bits: int = 1


cs = ConfigStore.instance()
cs.store(name="config", node=SerialPort)


@hydra.main(config_name="config")
def my_app(cfg: SerialPort) -> None:
    print(cfg)


if __name__ == "__main__":
    my_app()
