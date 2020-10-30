---
id: compose_api
title: Compose API
sidebar_label: Experimental compose API
---

Hydra 0.11.0 introduces a new experimental API for composing configuration via the `hydra.experimental.compose()` function.
Prior to calling compose(), you have to initialize Hydra: This can be done by using the standard `@hydra.main()` or by calling `hydra.experimental.initialize()`.

Here is an [example Jupyter notebook utilizing this API](https://github.com/facebookresearch/hydra/tree/0.11_branch/examples/notebook).

### `hydra.experimental.compose()` example
```python
from hydra.experimental import compose, initialize


if __name__ == "__main__":
    initialize(
        config_dir="conf", strict=True,
    )

    cfg = compose("config.yaml", overrides=["db=mysql", "db.user=me"])
    print(OmegaConf.to_yaml(cfg))
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


def initialize(config_dir=None, strict=None, caller_stack_depth=1):
    """
    Initializes the Hydra sub system

    :param config_dir: config directory relative to the calling script
    :param strict: Default value for strict mode
    :param caller_stack_depth:
    :return:
    """
```

