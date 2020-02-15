---
id: config_groups
title: Config groups
---

This example registers `mysql` and `postgresql` into the config group `db`.

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
When running this, you can now select which config group to use from the command line:
```yaml
$ python my_app.py db=mysql
db:
  driver: mysql
  host: localhost
  password: secret
  port: 3306
  user: omry
```

As a site note, you can model your configuration classes using inheritance, reducing the duplication between `mysql` and `postgresql`.
```python
@dataclass
class DBConfig:
    # In this example both configurations have a common default host
    host: str = "localhost"


@dataclass
class MySQLConfig:
    driver: str = "mysql"
    port: int = 3306
    user: str = "omry"
    password: str = "secret"

@dataclass
class PostGreSQLConfig:
    driver: str = "postgresql"
    port: int = 5432
    user: str = "postgre_user"
    password: str = "drowssap"
    timeout: int = 10
```