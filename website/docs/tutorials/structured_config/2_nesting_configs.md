---
id: nesting
title: Nesting configs
---
Configs can be nested using several different methods.

### Nesting using a dataclass definition
This is the preferred approach; use it when possible.
There are two things of note in this example:
- A top level `MyConfig` class defined and stored in the `ConfigStore`
- The `cfg` object in `my_app` is annotated as the top level `MyConfig` class, providing static type safety for 
the entire configuration tree
 
```python
@dataclass
class MySQLConfig:
    host: str = "localhost"
    port: int = 3306

@dataclass
class MyConfig:
    db: MySQLConfig = MySQLConfig()

cs = ConfigStore.instance()
cs.store(name="config", node=MyConfig)

@hydra.main(config_name="config")
def my_app(cfg: MyConfig) -> None:
    # Python knows that the type of cfg.db is MySQLConfig without any additional hints
    print(f"Host: {cfg.db.host}, port: {cfg.db.port}")

if __name__ == "__main__":
    my_app()
```

### Nesting by creating an ad-hoc config node
Ad-hoc config nodes can be created using Dictionaries.  While this
allows great flexibility, it offers reduced type safety.

```python
cfg_store.store(
    name="config",
    node={
        "src": MySQLConfig(host="localhost"),
        "dst": MySQLConfig(host="example.com"),
    },
)


@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(f"Copying {cfg.src.host}:{cfg.src.port} to {cfg.dst.host}:{cfg.dst.port}")
```
