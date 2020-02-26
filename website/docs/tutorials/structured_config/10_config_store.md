---
id: config_store
title: Config Store API
---
`ConfigStore` is a singleton storing configs in memory.
The primary API for interacting with the `ConfigStore` is the store method described below.

```python
class ConfigStore(metaclass=Singleton):
    def store(
        self,
        name: str,
        node: Any,
        group: Optional[str] = None,
        path: Optional[str] = None,
        provider: Optional[str] = None,
    ) -> None:
        """
        Stores a config node into the repository
        :param name: config name
        :param node: config node, can be DictConfig, ListConfig, Structured configs and even dict and list
        :param group: config group, subgroup separator is '/', for example hydra/launcher
        :param path: Config node parent hierarchy. child separator is '.', for example foo.bar.baz
        :param provider: the name of the module/app providing this config. Helps debugging.
        """
    ...
```
