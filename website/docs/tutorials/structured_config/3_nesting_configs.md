---
id: nesting
title: Nesting configs
---
Configs can be nested in several different ways.

#### Nesting using a dataclass definition
```python
@dataclass
class MySQLConfig:
    ...

@dataclass
class Config:
    db: MySQLConfig = MySQLConfig()
    verbose: bool = True

cfg_store = ConfigStore.instance()
cfg_store.store(node=Config, name="config")

@hydra.main(config_name="config")
def my_app(cfg: Config) -> None:
    # Python knows that the type of cfg.db is MySQLConfig without any additional hints
    print(
        f"Connecting to {cfg.db.driver} at {cfg.db.host}:{cfg.db.port}, "
        f"user={cfg.db.user}, password={cfg.db.password}"
    )


if __name__ == "__main__":
    my_app()

```
#### Nesting by specifying a node path
You may want to place MySQLConfig in a specific path in the final configuration object.
Use the path parameter to specify the path. You can use dot notation to create multiple
parent nodes (E.G. `path="foo.bar.baz"`)  

```python
@dataclass
class MySQLConfig:
    ...

cfg_store = ConfigStore.instance()
cfg_store.store(name="config", path="db", node=MySQLConfig)

@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    # In order to get type safety you need to tell
    # Python into thinking the type of cfg.db is MySQLConfig:
    db: MySQLConfig = cfg.db
    ...
```