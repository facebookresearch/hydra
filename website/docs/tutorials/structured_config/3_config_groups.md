---
id: config_groups
title: Config Groups
---
Structured Configs support config groups which are similar to file-based config groups.
The config options in config groups can be used as building blocks when composing the output config object.
One difference is that Structured Configs introduce runtime type safety which ensures that the resulting config object
adheres to the declared types.

This example adds `mysql` and `postgresql` configs into the Config Group `db`.
Like with config files, the configs in the `ConfigStore` acts as building blocks to be used when composing the 
output config object.

The type of variable `db` in the `Config` is `Any`. This allows both `MySQLConfig` and `PostGreSQLConfig` 
to be merged into it despite them not having a common superclass.

```python
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

# Config is extending DictConfig to allow type safe access to the pretty() function below
@dataclass
class Config(DictConfig):
    db: Any = MISSING

cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(group="db", name="mysql", node=MySQLConfig)
cs.store(group="db", name="postgresql", node=PostGreSQLConfig)

@hydra.main(config_name="config")
def my_app(cfg: Config) -> None:
    print(cfg.pretty())
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

#### Config inheritance
We can improve on the above example by modeling the configuration with inheritance.
Noteworthy things in the example:
- We can move fields to the top level class, reducing repetition of field names, type and default values.
- The type of the `db` field in `Config` is `DBConfig`. This ensures that only subclasses of `DBConfig` 
can be merged into db.
- We can use OmegaConf.get_type() to obtain the underlying type, and cast() to coerce the type checker to accept it.

```python
@dataclass
class DBConfig:
    host: str = "localhost"
    port: int = MISSING
    driver: str = MISSING

@dataclass
class MySQLConfig(DBConfig):
    driver = "mysql"
    port = 3306

@dataclass
class PostGreSQLConfig(DBConfig):
    driver = "postgresql"
    port = 5432
    timeout: int = 10

@dataclass
class Config(DictConfig):
    db: DBConfig = MISSING

cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(group="db", name="mysql", node=MySQLConfig)
cs.store(group="db", name="postgresql", node=PostGreSQLConfig)

def connect_mysql(cfg: MySQLConfig) -> None:
    print(f"Connecting to MySQL: {cfg.host}:{cfg.port}")

def connect_postgresql(cfg: PostGreSQLConfig) -> None:
    print(f"Connecting to PostGreSQL: {cfg.host}:{cfg.port} (timeout={cfg.timeout})")

@hydra.main(config_name="config")
def my_app(cfg: Config) -> None:
    # Remember that the actual type of Config and db inside it is DictConfig.
    # If you need to get the underlying type of a config object use OmegaConf.get_type:
    if OmegaConf.get_type(cfg.db) is MySQLConfig:
        connect_mysql(cast(MySQLConfig, cfg.db))
    elif OmegaConf.get_type(cfg.db) is PostGreSQLConfig:
        connect_postgresql(cast(PostGreSQLConfig, cfg.db))
    else:
        raise ValueError()
```

Example output:
```
$ python my_app_with_inheritance.py +db=postgresql
Connecting to PostGreSQL: localhost:5432 (timeout=10)
```