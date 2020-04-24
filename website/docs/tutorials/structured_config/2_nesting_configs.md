---
id: nesting
title: Nesting configs
---
Configs can be nested using several different methods.

### Nesting using a dataclass definition
This is the preferred approach, use it when possible.
There two things of note in this example:
- A top level `MyConfig` class is defined and stored in the `ConfigStore`
- The `cfg` object in `my_app` is annotated as the top level `MyConfig` class, providing static type safety for 
the entire configuration tree
 
```python
@dataclass
class MySQLConfig:
    host: str = "localhost"
    port: int = 3306

@dataclassz
class MyConfig:
    db: MySQLConfig = MySQLConfig()
    verbose: bool = True

cfg_store = ConfigStore.instance()
cfg_store.store(name="config", node=MyConfig)

@hydra.main(config_name="config")
def my_app(cfg: MyConfig) -> None:
    # Python knows that the type of cfg.db is MySQLConfig without any additional hints
    print(f"Host: {cfg.db.host}, port: {cfg.db.port}")

if __name__ == "__main__":
    my_app()
```

### Nesting by specifying a node path
If for some reason you do not want to have a top level config class, you can still place MySQLConfig 
in a specific path in the final configuration object. To do that, use the `path` parameter to specify the path.
You can use dot-notation to create multiple parent nodes as needed (E.G. `path="foo.bar.baz"`)  

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
Another choice, which offers even more flexibility is to create an ad-hoc config node and store it.
This allow you to control the shape of the config node, enabling things like having multiple config nodes in the config
object you are storing. This method should be used as a last resort as it offers the least static type safety.

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
    src: MySQLConfig = cfg.src
    dst: MySQLConfig = cfg.dst
    print(f"Copying {src.host}:{src.port} to {dst.host}:{dst.port}")
```
