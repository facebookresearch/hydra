---
id: minimal_example
title: Minimal example
---

There are three key elements in this example:
- A `@dataclass` describes the application's configuration
- `ConfigStore` manages the Structured Config
- `cfg` is `duck typed` as a `MySQLConfig` instead of a `DictConfig` 


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
    print(f"Host: {cfg.host}, port: {cfg.port}")

if __name__ == "__main__":
    my_app()
```

If you a typo in your code:
```python
@hydra.main(config_name="config")
def my_app(cfg: MySQLConfig) -> None:
    if cfg.pork == "80":  # pork should be of port!
        print("Is this a webserver?!")
```

Static type checkers like `mypy` can catch it:
```
$ mypy my_app_type_error.py
my_app_type_error.py:21: error: "MySQLConfig" has no attribute "pork"
Found 1 error in 1 file (checked 1 source file)
```

Hydra will catch runtime errors that `mypy` cannot, such as:

A type error in the code:
```
$ python my_app_type_error.py
Traceback (most recent call last):
...
omegaconf.errors.ConfigAttributeError: Key 'pork' not in 'MySQLConfig'
        full_key: pork
        reference_type=Optional[dict]
        object_type=MySQLConfig
```

A type error in the command line:
```
$ python my_app_type_error.py port=fail 
omegaconf.errors.ValidationError: Value 'fail' could not be converted to Integer
        full_key: port
        reference_type=Optional[dict]
        object_type=MySQLConfig
```

## Duck typing

The name [Duck typing](https://en.wikipedia.org/wiki/Duck_typing) comes from the phrase "If it walks like a duck, swims like a duck, and quacks like a duck, then it probably is a duck".
It can be useful when you care about the methods or attributes of an object, not the actual type of the object.

In the example above `cfg` is duck typed as `MySQLConfig`.
It is actually an instance of `DictConfig`. The duck typing enables static type checking by tools like Mypy or PyCharm.
This reduces development time by catching coding errors before you run your application.