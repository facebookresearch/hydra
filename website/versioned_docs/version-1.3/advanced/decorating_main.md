---
id: decorating_main
title: Decorating the main function
---

`@hydra.main` can be used over decorated functions:

<div className="row">
<div className="col col--6">

```python title="app.py"
from omegaconf import DictConfig, OmegaConf
import hydra

from mypackage import mydecorator

@hydra.main(version_base=None)
@mydecorator
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
```
</div>

<div className="col col--6">

```python title="mypackage.py"
from functools import wraps
from typing import Callable

from omegaconf import DictConfig

def mydecorator(func: Callable) -> Callable:
  @wraps(func)
  def inner_decorator(cfg: DictConfig):
    print(OmegaConf.to_yaml(cfg))  # do some stuff
    return func(cfg) # pass cfg to decorated function

  return inner_decorator
```

</div></div>

Decorator should be compatible with rules below:

1. It should be created using `@functools.wraps` decorator
2. It should accept an argument of type `omegaconf.DictConfig` and pass it to the underlying function

:::info
`@functools.wraps` passes name and docstring of underlying function to the decorated one.

But more importantly, it saves underlying function into `__wrapped__` attribute of decorated function,
which is used by `hydra.main` to calculate the absolute path of config file.

Without `@wraps` hydra will fail while searching for the config path:

```log
hydra.errors.MissingConfigException: Primary config directory not found.
Check that the config directory '/usr/local/lib/python3.7/conf' exists and readable
```

:::
