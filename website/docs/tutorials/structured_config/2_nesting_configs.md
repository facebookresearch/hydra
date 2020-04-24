---
id: nesting
title: Nesting configs
---
Configs can be nested in several different ways.

### Nesting using a dataclass definition
This is the preferred approach, use it when possible.
```python
@dataclass
class MySQLConfig:
    host: str = "localhost"
    port: int = 3306

@dataclass
class Config:
    db: MySQLConfig = MySQLConfig()
    verbose: bool = True

cfg_store = ConfigStore.instance()
cfg_store.store(name="config", node=Config)

@hydra.main(config_name="config")
def my_app(cfg: Config) -> None:
    # Python knows that the type of cfg.db is MySQLConfig without any additional hints
    print(f"Host: {cfg.db.host}, port: {cfg.db.port}")

if __name__ == "__main__":
    my_app()
```

### Nesting by specifying a node path
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
    # mypy does not know the type of cfg.db.
    # You can optionally help it with a hint to get static type checking.
    db: MySQLConfig = cfg.db
    print(f"Host: {db.host}, port: {db.port}")
```

### Nesting by creating an ad-hoc config node
You can also place MySQLConfig in a specific path by creating an ad-hoc config node that has it in that path.
This is more verbose than the two previous methods, but allow you to create more complex configs that can potentially
contain multiple nodes under the same config name.
This method should be used as a last resort.

```python
cfg_store = ConfigStore.instance()
cfg_store.store(name="config", node={"db": MySQLConfig})
```
