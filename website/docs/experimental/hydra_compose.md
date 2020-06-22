---
id: compose_api
title: Compose API
sidebar_label: Compose API
---

The compose API can compose a configuration similar to `@hydra.main()` anywhere in the code.  
Prior to calling compose(), you have to initialize Hydra: This can be done by using the standard `@hydra.main()`
or by calling one of the initialization methods listed below.

Compose is useful when `@hydra.main()` is not applicable.
### Examples
 - [Jupyter notebook with compose](https://github.com/facebookresearch/hydra/tree/master/examples/notebook) (hydra_notebook_example.ipynb)
 - [Unit testing with compose](https://github.com/facebookresearch/hydra/tree/master/examples/advanced/hydra_app_example/tests/test_hydra_app.py).

### Code example
```python
from hydra.experimental import compose, initialize


if __name__ == "__main__":
    initialize(config_path="conf")

    cfg = compose(config_name="config", overrides=["db=mysql", "db.user=me"])
    print(cfg.pretty())
```
### API Documentation
```python
def compose(config_file=None, overrides=[]):
    """
    :param config_file: optional config file to load
    :param overrides: list of overrides for config file
    :return: the composed config
    """
    ...

def initialize(
    config_path: Optional[str] = None,
    strict: Optional[bool] = None,
    caller_stack_depth: int = 1,
) -> None:
    """
    Initialize automatically detect the calling file or module.
    config_path is relative to the detected calling for or module.

    :param config_path: A directory relative to the declaring python file or module
    :param strict: (Deprecated), will be removed in the next major version
    :param caller_stack_depth: stack depth of module the config_path is relative to
    """

def initialize_with_file(
    file: Optional[str], config_path: Optional[str] = None
) -> None:
    """
    Initialize Hydra and add the config_path to the search path.
    The config path is relative to the calling_file.
    :param file : The file to make the config_path relative to
    :param config_path : The config path
    """
    ...

def initialize_with_module(
    module: Optional[str], config_path: Optional[str] = None
) -> None:
    """
    Initialize Hydra and add the config_path to the search path.
    The config path is relative to the calling_module.
    :param module : The module to make the config_path relative to
    :param config_path : The config path
    """
    ...
```

