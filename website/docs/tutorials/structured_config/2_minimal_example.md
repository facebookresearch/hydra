---
id: minimal_example
title: Minimal example
---

This tutorial uses `ConfigStore`, an in-memory Singleton that stores configurations.

The following example uses a `@dataclass` as the description of the application's configuration. 
As usual, `cfg` is an instance of `DictConfig`; declaring it's type as `MySQLConfig` enables static type checking by tools like Mypy or PyCharm.

```python
from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore

@dataclass
class MySQLConfig:
    host: str = "localhost"
    port: int = 3306

cfg_store = ConfigStore.instance()
# Registering the Config class with the name 'config'
cfg_store.store(node=MySQLConfig, name="config")

@hydra.main(config_name="config")
def my_app(cfg: MySQLConfig) -> None:
    # The real type of cfg is DictConfig. We lie to get static type checking.
    # See duck-typing section below for more information.
    print(f"Host: {cfg.host}, port: {cfg.port}")

if __name__ == "__main__":
    my_app()
```

If you have this error in your code:
```python {3}
@hydra.main(config_name="config")
def my_app(cfg: MySQLConfig) -> None:
    if cfg.post == "localhost":
        print("Home is where the heart is!")
```

Static type checkers like `mypy` can catch it:
```
$ mypy my_app_type_error.py 
my_app_type_error.py:21: error: "MySQLConfig" has no attribute "post"
Found 1 error in 1 file (checked 1 source file)
```

You also get runtime type checking:
```python
$ python my_app_type_error.py
Traceback (most recent call last):
...
omegaconf.errors.ConfigAttributeError: Key 'post' not in 'MySQLConfig'
        full_key: post
        reference_type=Optional[dict]
        object_type=MySQLConfig
```

Hydra will also catch runtime errors that `mypy` cannot:
```
$ python my_app_type_error.py port=fail
omegaconf.errors.ValidationError: Value 'fail' could not be converted to Integer
        full_key: port
        reference_type=Optional[dict]
        object_type=MySQLConfig
```

## Duck typing
If it swims like a duck and quacks like a duck, it's a "duck".
wikipedia.

blah