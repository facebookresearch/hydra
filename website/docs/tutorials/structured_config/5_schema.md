---
id: schema
title: Structured Config schema
---
[![Example](https://img.shields.io/badge/-Example-informational)](https://github.com/facebookresearch/hydra/tree/master/examples/tutorials/structured_configs/5_structured_config_schema/)

We have seen how to use Structured Configs as configuration, but they can also be used as a schema (i.e. validating configuration files).
To achieve this, we will follow the common pattern of [Extending Configs](../../patterns/extending_configs.md) - but instead of extending another config file,
we will extend a Structured Config.

This page shows how to validate the config files `config.yaml`, `db/mysql.yaml` and `db/postgresql.yaml` 
against a Structured Config schema.

## Validating against a schema in the same config group

Given the config directory structure:
```text
conf/
├── config.yaml
└── db
    ├── mysql.yaml
    └── postgresql.yaml
```

We will add Structured Config schema for each of the config files above and store in the 
Config Store as `base_config`, `db/base_mysql` and `db/base_postgresql`.

Then, we will use the Defaults List in each config to specify its base config as follows:

<div className="row">
<div className="col col--4">

```yaml title="config.yaml" {2}
defaults:
  - base_config
  - db: mysql


```

</div>
<div className="col col--4">

```yaml title="db/mysql.yaml" {2}
defaults:
  - base_mysql

user: omry
password: secret
```
</div>
<div className="col col--4">

```yaml title="db/postgresql.yaml" {2}
defaults:
  - base_postgresql

user: postgre_user
password: drowssap
```
</div>
</div>

Nothing much is new in the source code: 
<details><summary>my_app.py (Click to expand)</summary>

```python {27-29}
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
    db: DBConfig = MISSING

cs = ConfigStore.instance()
cs.store(name="base_config", node=Config)
cs.store(group="db", name="base_mysql", node=MySQLConfig)
cs.store(group="db", name="base_postgresql", node=PostGreSQLConfig)

@hydra.main(config_path="conf", config_name="config")
def my_app(cfg: Config) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()
```
</details>
<br/>
When Hydra composes the final config object, the schemas from the config store are used to 
validate that the both the configuration files and command line overrides are conforming to the schema. 

```
$ python my_app.py db.port=fail
Error merging override db.port=fail
Value 'fail' could not be converted to Integer
        full_key: db.port
        reference_type=Optional[MySQLConfig]
        object_type=MySQLConfig
```

## Validating against a schema from a different config group
In the above example, the schema we used was stored in the same config group.
This is not always the case, for example - A library might provide schemas in its own config group.

Here is a modified version of the example above, where a mock database_lib is providing the schemas
we want to validate against.


<div className="row">
<div className="col col--6">

```python title="my_app.py"
import database_lib


@dataclass
class Config:
    db: database_lib.DBConfig = MISSING

cs = ConfigStore.instance()
cs.store(name="base_config", node=Config)

# database_lib registers its configs
# in database_lib/db
database_lib.register_configs()


@hydra.main(
    config_path="conf",
    config_name="config",
)
def my_app(cfg: Config) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()

```
</div>
<div className="col col--6">

```python title="database_lib.py" {17,22}
@dataclass
class DBConfig:
  ...

@dataclass
class MySQLConfig(DBConfig):
  ...

@dataclass
class PostGreSQLConfig(DBConfig):
  ...


def register_configs() -> None:
    cs = ConfigStore.instance()
    cs.store(
        group="database_lib/db",
        name="mysql",
        node=MySQLConfig,
    )
    cs.store(
        group="database_lib/db",
        name="postgresql",
        node=PostGreSQLConfig,
    )

```
</div>
</div>

The Defaults List entry for the base config is slightly different:
<div className="row">
<div className="col col--6">

```yaml title="db/mysql.yaml" {2}
defaults:
  - /database_lib/db/mysql@_here_

user: omry
password: secret
```
</div>
<div className="col col--6">

```yaml title="db/postgresql.yaml" {2}
defaults:
  - /database_lib/db/postgresql@_here_

user: postgre_user
password: drowssap
```
</div>
</div>

- We refer to the config with an absolute path because it is outside the subtree of the db config group. 
- we override the package to `_here_` to ensure that the package of the schema is the same as the package 
  of the config it's validating.

