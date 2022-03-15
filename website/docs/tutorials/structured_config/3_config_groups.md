---
id: config_groups
title: Config Groups
---

import {ExampleGithubLink} from "@site/src/components/GithubLink"

<ExampleGithubLink to="examples/tutorials/structured_configs/3_config_groups/my_app.py"/>

Structured Configs can be used to implement config groups. Special care needs to be taken when specifying a 
default value for fields populated by a config group. We will look at why below.

```python title="Defining a config group for database" {16-17,22-23}
from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore

@dataclass
class MySQLConfig:
    driver: str = "mysql"
    host: str = "localhost"
    port: int = 3306

@dataclass
class PostGreSQLConfig:
    driver: str = "postgresql"
    host: str = "localhost"
    port: int = 5432
    timeout: int = 10

@dataclass
class Config:
    # We will populate db using composition.
    db: Any

# Create config group `db` with options 'mysql' and 'postgreqsl'
cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(group="db", name="mysql", node=MySQLConfig)
cs.store(group="db", name="postgresql", node=PostGreSQLConfig)

@hydra.main(version_base=None, config_name="config")
def my_app(cfg: Config) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()
```

:::caution
The *Config* class is **NOT** the Defaults list. We will see the Defaults list in the next page.
:::

You can select the database from the command line:
```yaml
$ python my_app.py +db=postgresql
db:
  driver: postgresql
  host: localhost
  password: drowssap
  port: 5432
  timeout: 10
  user: postgres_user
```

The `+` above is required because there is no default choice for the config group `db`.
The next page will reintroduce the Defaults List, eliminating the need for the `+`.

### Config inheritance

<ExampleGithubLink to="examples/tutorials/structured_configs/3_config_groups/my_app_with_inheritance.py"/>

Standard Python inheritance can be used to get improved type safety, and to move common fields to the parent class.

```python title="Defining a config group for database using inheritance"
from omegaconf import MISSING

@dataclass
class DBConfig:
    host: str = "localhost"
    port: int = MISSING
    driver: str = MISSING

@dataclass
class MySQLConfig(DBConfig):
    driver: str = "mysql"
    port: int = 3306

@dataclass
class PostGreSQLConfig(DBConfig):
    driver: str = "postgresql"
    port: int = 5432
    timeout: int = 10

@dataclass
class Config:
    # We can now annotate db as DBConfig which
    # improves both static and dynamic type safety.
    db: DBConfig
```

### Missing fields
Assign *MISSING* to a field to indicates that it does not have a default value. This is equivalent to
the `???` literal we have seen in OmegaConf configs before.

Omitting a default value is equivalent to assigning *MISSING* to it, although it is sometimes 
convenient to be able to assign MISSING it to a field.

:::caution
Do not confuse **omegaconf.MISSING** with **dataclass.MISSING**.
:::
