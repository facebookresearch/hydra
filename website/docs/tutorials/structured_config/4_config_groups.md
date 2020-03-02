---
id: config_groups
title: Config groups
---

This example adds `mysql` and `postgresql` configs into the config group `database`.

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
    timeout: int = 10
    user: str = "postgre_user"
    password: str = "drowssap"

# Config can extend DictConfig to allow type safe access to DictConfig functions.
@dataclass
class Config(DictConfig):
    db: Any = MySQLConfig()

cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(group="database", name="mysql", path="db", node=MySQLConfig)
cs.store(group="database", name="postgresql", path="db", node=PostGreSQLConfig)

@hydra.main(config_name="config")
def my_app(cfg: Config) -> None:
    print(cfg.pretty())

if __name__ == "__main__":
    my_app()

```
You can change the default database from the command line:
```yaml
$ python my_app.py database=postgresql
db:
  driver: postgresql
  host: localhost
  password: drowssap
  port: 5432
  timeout: 10
  user: postgre_user
```

#### Config inheritance
You can also model your configuration classes using inheritance.

```python
@dataclass
class DBConfig:
    host: str = "localhost"
    driver: str = MISSING
    port: int = MISSING
    user: str = MISSING
    password: str = MISSING

@dataclass
class MySQLConfig(DBConfig):
    driver = "mysql"
    port = 3306
    user = "omry"
    password = "secret"

@dataclass
class PostGreSQLConfig(DBConfig):
    driver = "postgresql"
    port = 5432
    user = "postgre_user"
    password = "drowssap"
    # new field:
    timeout: int = 10
```