---
id: config_store
title: Config Store API
---
ConfigStore and SchemaStore are singletons storing configs in memory.
Each is used differently, but they are sharing the same store() API,

```python
def store(
    self,
    name: str,
    node: Any,
    group: Optional[str] = None,
    path: Optional[str] = None,
) -> None:
    """
    Stores a config node into the repository
    :param name: config name
    :param node: config node, can be DictConfig, ListConfig, Structured Configs and even dict and list
    :param group: config group, subgroup separator is '/', for example hydra/launcher
    :param path: Config node parent hierarchy. child separator is '.', for example foo.bar.baz
    """
    ...
```