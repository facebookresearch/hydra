---
id: config_groups
title: Config groups
---

Using the path parameter can be handy, but it's even better if you create a top level config that describes the complete structure.
The example below nests MySQLConfig inside a Config class, and registers the top level Config as "config":

```python
@dataclass
class MySQLConfig:
    driver: str = "mysql"
    host: str = "localhost"
    port: int = 3306
    user: str = "omry"
    password: str = "secret"

@dataclass
class PostGreSQLConfig:
    driver: str = "postgresql"
    host: str = "localhost"
    port: int = 5432
    user: str = "postgre_user"
    password: str = "drowssap"
    timeout: int = 10

# Config is extending DictConfig to allow type safe access to the pretty() function below.
@dataclass
class Config(DictConfig):
    db: Any = MISSING

cs = ConfigStore.instance()
cs.store(group="db", name="mysql", path="db", node=MySQLConfig)
cs.store(group="db", name="postgresql", path="db", node=PostGreSQLConfig)
cs.store(name="config", node=Config)


@hydra.main(config_name="config")
def my_app(cfg: Config) -> None:
    print(cfg.pretty())


if __name__ == "__main__":
    my_app()

```

You can also model your configuration classes using inheritance:
```python
@dataclass
class DBConfig:
    driver: str = MISSING
    host: str = "localhost"
    port: int = 3306
    user: str = "omry"
    password: str = "secret"


@dataclass
class MySQLConfig(DBConfig):
    driver: str = "mysql"


@dataclass
class PostGreSQLConfig(DBConfig):
    driver: str = "postgresql"
    timeout: int = 10

```