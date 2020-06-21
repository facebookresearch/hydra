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
 - [Jupyter notebook with compose](https://github.com/facebookresearch/hydra/tree/master/examples/jupyter-notebooks) (hydra_notebook_example.ipynb)
 - [Unit testing with compose](https://github.com/facebookresearch/hydra/tree/master/examples/advanced/hydra_app_example/tests/test_hydra_app.py).

### Code example
```python
from hydra.experimental import compose, initialize


if __name__ == "__main__":
    initialize(config_path="conf", job_name="test_app")

    cfg = compose(config_name="config", overrides=["db=mysql", "db.user=me"])
    print(cfg.pretty())
```
### API Documentation
```python
def compose(
    config_name: Optional[str] = None,
    overrides: List[str] = [],
    strict: Optional[bool] = None,
    return_hydra_config: bool = False,
) -> DictConfig:
    """
    :param config_name: the name of the config (usually the file name without the .yaml extension)
    :param overrides: list of overrides for config file
    :param strict: optionally override the default strict mode
    :param return_hydra_config: True to return the hydra config node in the resulting config
    :return: the composed config
    """

def initialize(
    config_path: Optional[str] = None,
    job_name: Optional[str] = "app",
    strict: Optional[bool] = None,
    caller_stack_depth: int = 1,
) -> None:
    """
    Initializes Hydra and add the config_path to the config search path.
    config_path is relative to the parent of the caller.
    Hydra detects the caller type automatically at runtime.
    Supported callers:
    - Python scripts
    - Python modules
    - Unit tests
    - Jupyter notebooks.
    :param config_path: path relative to the caller
    :param job_name: the value for hydra.job.name (default is 'app')
    :param strict: (Deprecated), will be removed in the next major version
    :param caller_stack_depth: stack depth of the caller, defaults to 1 (direct caller).
    """

def initialize_config_module(config_module: str, job_name: str = "app") -> None:
    """
    Initializes Hydra and add the config_module to the config search path.
    The config module must be importable (an __init__.py must exist at its top level)
    :param config_module: absolute module name, for example "foo.bar.conf".
    :param job_name: the value for hydra.job.name (default is 'app')
    """

def initialize_config_dir(
    config_dir: str, job_name: Optional[str] = None, caller_stack_depth: int = 1,
) -> None:
    """
    Initializes Hydra and add the config_path to the config search path.
    The config_path is always a path on the file system.
    The config_path can either be an absolute path on the file system or a file relative to the caller.
    Supported callers:
    - Python scripts
    - Unit tests
    - Jupyter notebooks.
    If the caller is a Python module and the config dir is relative an error will be raised.
    :param config_dir: file system path relative to the caller or absolute
    :param job_name: Optional job name to use instead of the automatically detected one
    :param caller_stack_depth: stack depth of the caller, defaults to 1 (direct caller).
    """
```

