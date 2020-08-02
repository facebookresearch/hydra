---
id: instantiate_with_structured_config
title: Structured Configs with instantiate
sidebar_label: Structured Configs with instantiate
---

Structured Configs can be used with `hydra.utils.instantiate()`. A complete, standalone example is available [here](https://github.com/facebookresearch/hydra/tree/master/examples/patterns/instantiate/structured_configs).

<div className="row">

<div className="col col--6">

#### Example usage

```python title="my_app.py" {18}

# Base class for the database config
@dataclass
class DBConfig:
    host: str = "localhost"
    port: int = 80


@dataclass
class MySQLConfig(DBConfig):
    port: int = 1234

@dataclass
class PostGreSQLConfig(DBConfig):
    port: int = 5678

defaults = [
    # Load the config "mysql" from the config group "db"
    {"db": "mysql",}
]


@dataclass
class Config(DictConfig):
    defaults: List[Any] = field(default_factory=lambda: defaults)
    db: ObjectConf = MISSING


cs = ConfigStore.instance()
cs.store(name="config", node=Config)
cs.store(
    group="db",
    name="mysql",
    node=ObjectConf(target="my_app.MySQLConnection", params=MySQLConfig,),
)
cs.store(
    group="db",
    name="postgresql",
    node=ObjectConf(target="my_app.PostgreSQLConnection", params=PostGreSQLConfig,),
)


@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    connection = instantiate(cfg.db)
    connection.connect()

if __name__ == "__main__":
    my_app()
```

</div>

<div className="col col--6">

#### Sample Output

```bash
$ python my_app.py
MySQL connecting on port=1234
```

```bash
$ python my_app.py db=postgresql
PostgreSQL connecting on port=5678
```

</div>
</div>