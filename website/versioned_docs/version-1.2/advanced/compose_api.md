---
id: compose_api
title: Compose API
sidebar_label: Compose API
---

import GithubLink,{ExampleGithubLink} from "@site/src/components/GithubLink"

The compose API can compose a config similarly to `@hydra.main()` anywhere in the code.  
Prior to calling compose(), you have to initialize Hydra: This can be done by using the standard `@hydra.main()`
or by calling one of the initialization methods listed below.

### When to use the Compose API

The Compose API is useful when `@hydra.main()` is not applicable.
For example:

- Inside a Jupyter notebook ([Example](jupyter_notebooks.md))
- Inside a unit test ([Example](unit_testing.md))
- In parts of your application that does not have access to the command line (<GithubLink to="examples/advanced/ad_hoc_composition">Example</GithubLink>).
- To compose multiple configuration objects (<GithubLink to="examples/advanced/ray_example/ray_compose_example.py">Example with Ray</GithubLink>).

<div class="alert alert--info" role="alert">
Please avoid using the Compose API in cases where <b>@hydra.main()</b> can be used.  
Doing so forfeits many of the benefits of Hydra
(e.g., Tab completion, Multirun, Working directory management, Logging management and more)
</div>

### Initialization methods
There are 3 initialization methods:
- `initialize()`: Initialize with a config path relative to the caller
- `initialize_config_module()` : Initialize with config_module (absolute)
- `initialize_config_dir()` : Initialize with a config_dir on the file system (absolute)

All 3 can be used as methods or contexts.
When used as methods, they are initializing Hydra globally and should only be called once.
When used as contexts, they are initializing Hydra within the context can be used multiple times.
Like <b>@hydra.main()</b> all three support the [version_base](../upgrades/version_base.md) parameter
to define the compatibility level to use.

### Code example
```python
from hydra import compose, initialize
from omegaconf import OmegaConf

if __name__ == "__main__":
    # context initialization
    with initialize(version_base=None, config_path="conf", job_name="test_app"):
        cfg = compose(config_name="config", overrides=["db=mysql", "db.user=me"])
        print(OmegaConf.to_yaml(cfg))

    # global initialization
    initialize(version_base=None, config_path="conf", job_name="test_app")
    cfg = compose(config_name="config", overrides=["db=mysql", "db.user=me"])
    print(OmegaConf.to_yaml(cfg))
```
### API Documentation

```python title="Compose API"
def compose(
    config_name: Optional[str] = None,
    overrides: List[str] = [],
    return_hydra_config: bool = False,
) -> DictConfig:
    """
    :param config_name: the name of the config
           (usually the file name without the .yaml extension)
    :param overrides: list of overrides for config file
    :param return_hydra_config: True to return the hydra config node in the result
    :return: the composed config
    """
```

```python title="Relative initialization"
def initialize(
    version_base: Optional[str],
    config_path: Optional[str] = None,
    job_name: Optional[str] = "app",
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
    :param version_base: compatibility level to use.
    :param config_path: path relative to the parent of the caller
    :param job_name: the value for hydra.job.name (By default it is automatically detected based on the caller)
    :param caller_stack_depth: stack depth of the caller, defaults to 1 (direct caller).
    """
```

```python title="Initialzing with config module"
def initialize_config_module(
    config_module: str,
    version_base: Optional[str],
    job_name: str = "app"
) -> None:
    """
    Initializes Hydra and add the config_module to the config search path.
    The config module must be importable (an __init__.py must exist at its top level)
    :param config_module: absolute module name, for example "foo.bar.conf".
    :param version_base: compatibility level to use.
    :param job_name: the value for hydra.job.name (default is 'app')
    """
```
```python title="Initialzing with config directory"
def initialize_config_dir(
    config_dir: str,
    version_base: Optional[str],
    job_name: str = "app"
) -> None:
    """
    Initializes Hydra and add an absolute config dir to the to the config search path.
    The config_dir is always a path on the file system and is must be an absolute path.
    Relative paths will result in an error.
    :param config_dir: absolute file system path
    :param version_base: compatibility level to use.
    :param job_name: the value for hydra.job.name (default is 'app')
    """
```

