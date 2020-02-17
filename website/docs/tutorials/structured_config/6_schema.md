---
id: schema
title: Structured config as schema
---
We have seen how to use Structured Configs as configuration, but they can also be used as a schema validating configuration files!

`SchemaStore` can be used to store schemas. It is very similar to The `ConfigStore` class we saw earlier.
When Hydra loads a configuration, it looks for schema with the same name in the `SchemaStore`. If found, it is used as the schema for the newly loaded config.

This is an example of defining and registering one schema for db/mysql and another for db/postgresql.

```python
from dataclasses import dataclass

from omegaconf import MISSING, DictConfig

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class DBConfig:
    driver: str = MISSING
    host: str = "localhost"
    port: int = MISSING


@dataclass
class MySQLConfig(DBConfig):
    driver: str = "mysql"
    port: int = 3306
    user: str = MISSING
    password: str = MISSING


@dataclass
class PostGreSQLConfig(DBConfig):
    driver: str = "postgresql"
    port: int = 5432
    user: str = MISSING
    password: str = MISSING
    timeout: int = 10


# registering db/mysql and db/postgresql schemas.
ss = ConfigStore.instance()
ss.store(group="db", name="mysql", path="db", node=MySQLConfig)
ss.store(group="db", name="postgresql", path="db", node=PostGreSQLConfig)


# config here is config.yaml under the conf directory.
# config.yaml will compose in db: mysql by default (per the defaults list),
# and it will be validated against the schema
@hydra.main(config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(cfg.pretty())


if __name__ == "__main__":
    my_app()
```

`@hydra.main()` above is specifying a config_path and a config_name.
This is what the conf directory looks like:
```text
$ tree conf/
conf/
├── config.yaml
└── db
    ├── mysql.yaml
    └── postgresql.yaml
```

When `db/mysql.yaml` and `db/postgresql.yaml` are loaded, the corresponding schemas from the `SchemaStore` are used automatically.
This can be used to validate that both the configuration files (`mysql.yaml` and `postgresql.yaml`) and the command line overrides are conforming to the schema. 

```bash
$ python my_app.py  db.port=fail
Traceback (most recent call last):
..
omegaconf.errors.ValidationError: Error setting 'db.port = fail' : Value 'fail' could not be converted to Integer
```