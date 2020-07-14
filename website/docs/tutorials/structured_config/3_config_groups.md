---
id: config_groups
title: Config Groups
---
Structured Configs can be used to implement config groups. Special care needs to be taken when specifying a 
default value for a config group. We will look at why below.

```python title="Defining a config group for database" {16-17,22-23}
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
    # Keep db MISSING. We will populate it using composition.
    db: Any = MISSING

# Create config group `db` with options 'mysql' and 'postgreqsl'
cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(group="db", name="mysql", node=MySQLConfig)
cs.store(group="db", name="postgresql", node=PostGreSQLConfig)

@hydra.main(config_name="config")
def my_app(cfg: Config) -> None:
    # cast cfg to DictConfig to get type safe access to pretty()
    print(cast(DictConfig, cfg).pretty())
```

You can select the database from the command line:
```yaml
$ python my_app.py +db=postgresql
db:
  driver: postgresql
  host: localhost
  password: drowssap
  port: 5432
  timeout: 10
  user: postgre_user
```

In the above example we need the `+` because there is no default choice for which config to load in the `db` group, so we are effectively _adding_ a new config element rather than _overriding_ an existing one.
The next page in this tutorial will show how to add such a default choice, thus removing the need for `+` on the command line.

### Config inheritance
Standard Python inheritance can be used to get improved type safety, and to move common fields to the parent class.

```python title="Defining a config group for database using inheritance"
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
    db: DBConfig = MISSING
```
