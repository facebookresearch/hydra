---
id: schema
title: Structured config schema
---
We have seen how to use Structured Configs as configuration, but they can also be used as a schema validating configuration files!
When Hydra loads a configuration, it looks for config with the same name in the `ConfigStore`.
If found, it is used as the schema for the newly loaded config.

This is an example of defining and stores one schema for db/mysql and another for db/postgresql.

Given a config directory structure like:
```text
$ tree conf/
conf/
├── config.yaml
└── db
    ├── mysql.yaml
    └── postgresql.yaml
```

The Structurd Configs below are stored as db/mysql and db/postgresql. They will be used as schema
when we load the corresponding config files.

```python
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
ss.store(group="db", name="mysql", node=MySQLConfig)
ss.store(group="db", name="postgresql", node=PostGreSQLConfig)


# config here is config.yaml under the conf directory.
# config.yaml will compose in db: mysql by default (per the defaults list),
# and it will be validated against the schema
@hydra.main(config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    ...
```


When `db/mysql.yaml` and `db/postgresql.yaml` are loaded, the corresponding configs from the `ConfigStore` are used automatically.
This can be used to validate that both the configuration files (`mysql.yaml` and `postgresql.yaml`) and the command line overrides are conforming to the schema. 

```
$ python my_app.py db.port=fail
Error merging override db.port=fail
Value 'fail' could not be converted to Integer
        full_key: db.port
        reference_type=Optional[MySQLConfig]
        object_type=MySQLConfig
```