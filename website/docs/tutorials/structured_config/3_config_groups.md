---
id: config_groups
title: Config groups
---

This example adds `mysql` and `postgresql` configs into the config group `database`.
Noteworthy things in the example:
 - Despite their similarity, The two config classes `MySQLConfig` and `PostGreSQLConfig` are independent
 - The type of the `db` field in `Config` is `Any`, This means it offers no static or runtime type safety

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

# Config is extending DictConfig to allow type safe access to the pretty() function below.
@dataclass
class Config(DictConfig):
    db: Any = MISSING

cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(group="database", name="mysql", path="db", node=MySQLConfig)
cs.store(group="database", name="postgresql", path="db", node=PostGreSQLConfig)

@hydra.main(config_name="config")
def my_app(cfg: Config) -> None:
    print(cfg.pretty())
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
We can improve on the above example by modeling the configuration with inheritance.
Noteworthy things in the example:
- We can move fields to the top level class, reducing repetition of field names, type and default values
- The type of the `db` field in `Config` is `DBConfig`, this offers static and runtime type safety 
- We use OmegaConf.get_type() to obtain the underlying type, and cast() to coerce the type checker to accept it

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
cs.store(group="database", name="mysql", path="db", node=MySQLConfig)
cs.store(group="database", name="postgresql", path="db", node=PostGreSQLConfig)

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