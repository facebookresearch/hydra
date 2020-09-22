# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import hydra

# Generated config dataclasses
from example.config.configen.samples.my_module import AdminConf, UserConf
from hydra.core.config_store import ConfigStore
from omegaconf import DictConfig

# Underlying objects
from configen.samples.my_module import Admin, User

ConfigStore.instance().store(
    name="config",
    node={
        "user": UserConf,
        "admin": AdminConf,
    },
)


@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    user: User = hydra.utils.instantiate(cfg.user)
    admin: Admin = hydra.utils.instantiate(cfg.admin)
    print(user)
    print(admin)


if __name__ == "__main__":
    my_app()
