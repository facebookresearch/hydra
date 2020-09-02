---
id: schema
title: Structured config schema
---
[![Example](https://img.shields.io/badge/-Example-informational)](https://github.com/facebookresearch/hydra/tree/master/examples/tutorials/structured_configs/5_structured_config_schema/)

We have seen how to use Structured Configs as configuration, but they can also be used as a schema (i.e. validating configuration files).

When Hydra loads a config file, it looks in the `ConfigStore` for a Structured Config with a matching name and group.
If found, it is used as the schema for the newly loaded config.
 
This page shows how to validate `db/mysql.yaml` and `db/postgresql.yaml` files against a pre-defined schema.

Given the config directory structure:
```text
conf/
├── config.yaml
└── db
    ├── mysql.yaml
    └── postgresql.yaml
```

We can add Structured Configs for `mysql.yaml` and `postgresql.yaml`, providing a schema for validating them.


The Structured Configs below are stored as `db/mysql` and `db/postgresql`. They will be used as schema
when we load their corresponding config files.

```python title="my_app.py"
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
    user: str = MISSING
    port: int = 5432
    password: str = MISSING
    timeout: int = 10

@dataclass
class Config:
    # Note the lack of defaults list here.
    # In this example it comes from config.yaml
    db: DBConfig = MISSING

cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(group="db", name="mysql", node=MySQLConfig)
cs.store(group="db", name="postgresql", node=PostGreSQLConfig)

# The config name matches both 'config.yaml' under the conf directory
# and 'config' stored in the ConfigStore.
# config.yaml will compose in db: mysql by default (per the defaults list),
# and it will be validated against the schema from the Config class
@hydra.main(config_path="conf", config_name="config")
def my_app(cfg: Config) -> None:
    print(OmegaConf.to_yaml(cfg))
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

Unlike the example in the previous page, the Defaults List here is `config.yaml` and **not** in the `Config` class.
```yaml title="config.yaml"
defaults:
  - db: mysql
```
