# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra

# Underlying object
from configen.samples.user import User

# Generated config dataclass
from example.gen.configen.samples.user.conf.User import UserConf
from hydra.core.config_store import ConfigStore

ConfigStore.instance().store(name="config", node={"user": UserConf})


@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    user: User = hydra.utils.instantiate(cfg.user)
    print(user)


if __name__ == "__main__":
    my_app()
