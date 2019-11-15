---
id: compose_api
title: Compose API
sidebar_label: Experimental compose API
---

Hydra 0.11.0 introduces a new experimental API that will allow composition of config from any place in the code via the `hydra.experimental.compose()` function.
Before using this function, you need to initialize Hydra. This can be done by using the standard `@hydra.main()` or by calling `hydra.experimental.initialize_hydra()`.

### `hydra.experimental.compose()` example
```python
from hydra.experimental import compose, initialize_hydra


if __name__ == "__main__":
    initialize_hydra(
        task_name="my_app", search_path_dir="conf", strict=True,
    )

    cfg = compose("config.yaml", overrides=["db=mysql", "db.user=me"])
    print(cfg.pretty())
```
### API Documentation
```python
def compose(config_file=None, overrides=[], strict=None):
    """
    :param config_file: optional config file to load
    :param overrides: list of overrides for config file
    :param strict: optionally override the default strict mode
    :return: the composed config
    """


def initialize_hydra(task_name, search_path_dir, strict):
    """
    Initializes the Hydra sub system

    :param task_name: The name of the task
    :param search_path_dir: entry point search path element (eg: /foo/bar or pkg://foo.bar)
    :param strict: Default value for strict mode
    """


```

