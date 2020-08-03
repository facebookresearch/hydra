---
id: instantiate_with_structured_config
title: Structured Configs with instantiate
sidebar_label: Structured Configs with instantiate
---

Structured Configs can be used with `hydra.utils.instantiate()`. A complete, standalone example is available [here](https://github.com/facebookresearch/hydra/tree/master/examples/patterns/instantiate/structured_configs).

#### Example usage

```python title="my_app.py"

# Base class for the database config
@dataclass
class DBConfig:
    driver: MISSING
    host: str = "localhost"
    port: int = 80

@dataclass
class MySQLConfig(DBConfig):
    driver: str = "MySQL"
    port: int = 1234

@dataclass
class PostGreSQLConfig(DBConfig):
    driver: str = "PostgreSQL"
    port: int = 5678
    timeout: int = 10

defaults = [{"db": "mysql",}]

@dataclass
class Config(DictConfig):
    defaults: List[Any] = field(default_factory=lambda: defaults)
    db: ObjectConf = MISSING

cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(
    group="db",
    name="mysql",
    node=ObjectConf(target="my_app.MySQLConnection", params=MySQLConfig),
)
cs.store(
    group="db",
    name="postgresql",
    node=ObjectConf(target="my_app.PostgreSQLConnection", params=PostGreSQLConfig),
)

@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    connection = instantiate(cfg.db)
    connection.connect()

if __name__ == "__main__":
    my_app()
```


#### Sample Output

<div className="row">

<div className="col col--6">

```bash
$ python my_app.py
MySQL connecting to localhost:1234
```

</div>

<div className="col col--6">

```bash
$ python my_app.py db=postgresql
PostgreSQL connecting to localhost:5678
```

</div>
</div>