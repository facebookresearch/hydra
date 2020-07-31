---
id: instantiate_with_structured_config
title: Structured Configs with instantiate
sidebar_label: Structured Configs with instantiate
---

Structured Configs can be used with `hydra.utils.instantiate()`. A complete, standalone example is available [here](https://github.com/facebookresearch/hydra/tree/master/examples/patterns/instantiate/structured_configs).

#### Example usage

my_app.py
```python

# Base class for the database config
@dataclass
class DBConfig:
    host: str = "localhost"
    port: int = 80
    user: str = MISSING
    password: str = "1234"


@dataclass
class MySQLConfig(DBConfig):
    user: str = "root"
    password: str = "1234"


@dataclass
class PostGreSQLConfig(DBConfig):
    user: str = "root"
    password: str = "1234"
    database: str = "tutorial"

defaults = [
    # Load the config "mysql" from the config group "db"
    {"db": "mysql",}
]


@dataclass
class Config(DictConfig):
    defaults: List[Any] = field(default_factory=lambda: defaults)
    db: ObjectConf = MISSING


cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(
    group="db",
    name="mysql",
    node=ObjectConf(
        target="examples.patterns.instantiate.structured_config.my_app.MySQLConnection",
        params=MySQLConfig,
    ),
)
cs.store(
    group="db",
    name="postgresql",
    node=ObjectConf(
        target="examples.patterns.instantiate.structured_config.my_app.PostgreSQLConnection",
        params=PostGreSQLConfig,
    ),
)

def connect(cfg: DBConfig):
  ...

@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
  connection = hydra.utils.instantiate(cfg)
    ...

if __name__ == "__main__":
    my_app()
```
