---
id: nesting
title: Nesting configs
---

Using the path parameter can be handy, but it's even better if you create a top level config that describes the complete structure.
The example below nests MySQLConfig inside a Config class, and stores the top level Config as "config":

```python
@dataclass
class MySQLConfig:
    ...

@dataclass
class Config:
    db: MySQLConfig = MySQLConfig()

cfg_store = ConfigStore.instance()
# We no longer need to use the path parameter because Config has the correct structure
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