---
id: config_store
title: Config Store API
---
ConfigStore is a core Hydra singleton that maintaining configs in memory.
These configs can be used by Hydra when composing configuration objects and and should be populated ahead of time.
The primary user API in ConfigStore class is store() function:

```python
class ConfigStore(metaclass=Singleton):
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
        :param node: config node, can be DictConfig, ListConfig, Structured configs and even dict and list
        :param group: config group, subgroup separator is '/', for example hydra/launcher
        :param path: Config node parent hierarchy. child separator is '.', for example foo.bar.baz
        """
        ...
```