---
id: node_path
title: Custom node path
---

You may want to place MySQLConfig in a specific path in the final configuration object.
Use the path parameter to specify the path. You can use dot notation to create multiple
parent nodes (E.G. `path="foo.bar.baz"`)  

```python
class MySQLConfig:
    ...

cfg_store = ConfigStore.instance()
cfg_store.store(node=MySQLConfig, name="config", path="db")

@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    # In order to get type safety you need to fool Python into thinking the type of cfg.db is MySQLConfig:
    db: MySQLConfig = cfg.db
    print(
        f"Connecting to {db.driver} at {db.host}:{db.port}, user={db.user}, password={db.password}"
    )


if __name__ == "__main__":
    my_app()

```