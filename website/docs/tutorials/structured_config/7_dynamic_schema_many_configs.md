---
id: dynamic_schema
title: Dynamic schema with many configs
---
[![Example](https://img.shields.io/badge/-Example-informational)](https://github.com/facebookresearch/hydra/tree/master/examples/tutorials/structured_configs/7_dynamic_schema_many_configs/)

In this page we will see how to get runtime type safety for configs with dynamic schema.
Our top level config contains a single field - `db`, with the type `DBConfig`.
Based on user choice, we would like its type to be either `MySQLConfig` or `PostGreSQLConfig` at runtime.
The two schemas differs: config files that are appropriate for one are inappropriate for the other.

For each of the two schemas, we have two options - one for prod and one for staging:
```text title="Config directory"
├── config.yaml
└── db
    ├── mysql_prod.yaml
    ├── mysql_staging.yaml
    ├── postgresql_prod.yaml
    └── postgresql_staging.yaml
```

```python title="my_app.py"
@dataclass
class DBConfig:
    driver: str = MISSING
    host: str = MISSING

@dataclass
class MySQLConfig(DBConfig):
    driver: str = "mysql"
    encoding: str = MISSING

@dataclass
class PostGreSQLConfig(DBConfig):
    driver: str = "postgresql"
    timeout: int = MISSING

@dataclass
class Config:
    db: DBConfig = MISSING

cs = ConfigStore.instance()
cs.store(group="schema/db", name="mysql", node=MySQLConfig, package="db")
cs.store(group="schema/db", name="postgresql", node=PostGreSQLConfig, package="db")
cs.store(name="config", node=Config)

@hydra.main(config_path="conf", config_name="config")
def my_app(cfg: Config) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()
```

When composing the config, we need to select both the schema and the actual config group option.
This is what the defaults list looks like:

```yaml title="config.yaml"
defaults:
  - schema/db: mysql
  - db: mysql_staging
```

Let's dissect the how we store the schemas into the `ConfigStore`:
```python
cs.store(group="schema/db", name="mysql", node=MySQLConfig, package="db")
```

There are several notable things here:
- We use the group `schema/db` and not `db`.  
Config Groups are mutually exclusive, only one option can be selected from a Config Group. We want to select both the schema and the config.
Storing all schemas in subgroups of the config group schema is good practice. This also helps in preventing name collisions.
- We need to specify the package to be `db`.
By default, the package for configs stored in the `ConfigStore` is `_group_`. We want to schematize `db` and not `schema.db` in the config so we have to override that. 


By default, we get the mysql staging config:
```text title="$ python my_app.py"
db:
  driver: mysql
  host: mysql001.staging
  encoding: utf-8
```

We can change both the schema and the config: 
```text title="$ python my_app.py schema/db=postgresql db=postgresql_prod"
db:
  driver: postgresql
  host: postgresql01.prod
  timeout: 10
```

If we try to use a postgresql config without changing the schema as well we will get an error:
```text title="$ python my_app.py db=postgresql_prod"
Error merging db=postgresql_prod
Key 'timeout' not in 'MySQLConfig'
        full_key: db.timeout
        reference_type=DBConfig
        object_type=MySQLConfig
```
