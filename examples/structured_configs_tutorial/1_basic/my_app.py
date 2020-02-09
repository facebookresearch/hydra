# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class MySQLConfig:
    driver: str = "mysql"
    host: str = "localhost"
    port: int = 3306
    user: str = "omry"
    password: str = "secret"


cfg_store = ConfigStore.instance()
# Registering the Config class with the name 'config'
cfg_store.store(node=MySQLConfig, name="config")

# You can also register objects of this class like Config(port=8081)
# (If you are registering 'config' more than once the last one will replace the previous ones.
cfg_store.store(node=MySQLConfig(user="root", password="1234"), name="config")


# The config name can be used to indicate which config we are using
# Tye real type of cfg is actually DictConfig, but we lie a little to get static type checking.
# If it swims like a duck and quacks like a duck...
# You get the rest of the Hydra features, command line overrides, tab completion etc.
# In addition, you get runtime type safety! (you cannot assign a non integer value to cfg.port)
@hydra.main(config_name="config")
def my_app(cfg: MySQLConfig) -> None:
    print(
        f"Connecting to {cfg.driver} at {cfg.host}:{cfg.port}, user={cfg.user}, password={cfg.password}"
    )


if __name__ == "__main__":
    my_app()
