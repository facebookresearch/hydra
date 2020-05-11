---
id: minimal_example
title: Minimal example
---

There are three key elements in this example:
- A `@dataclass` describes the application's configuration
- `ConfigStore` manages the Structured Config. The config name `config` corresponds to the config filename `config.yaml` from the config-file based examples. 
- `cfg` is `duck typed` as a `MySQLConfig` instead of a `DictConfig` 


```python
from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore

@dataclass
class MySQLConfig:
    host: str = "localhost"
    port: int = 3306

cs = ConfigStore.instance()
# Registering the Config class with the name 'config'. 
cs.store(name="config", node=MySQLConfig)

@hydra.main(config_name="config")
def my_app(cfg: MySQLConfig) -> None:
    print(f"Host: {cfg.host}, port: {cfg.port}")

if __name__ == "__main__":
    my_app()
```

If you have a typo in your code, such as pork in the following example:
```python
@hydra.main(config_name="config")
def my_app(cfg: MySQLConfig) -> None:
    # pork should be port!
    if cfg.pork == 80:
        print("Is this a webserver?!")
```

Static type checkers like `mypy` can catch it:
```
$ mypy my_app_type_error.py
my_app_type_error.py:21: error: "MySQLConfig" has no attribute "pork"
Found 1 error in 1 file (checked 1 source file)
```

With structured configs, Hydra will catch these and runtime errors that mypy cannot, such as:

A type error in the code:
```
$ python my_app_type_error.py
Traceback (most recent call last):
...
omegaconf.errors.ConfigAttributeError: Key 'pork' not in 'MySQLConfig'
        full_key: pork
        reference_type=Optional[MySQLConfig]
        object_type=MySQLConfig
```

A type error in the command line:
```
$ python my_app_type_error.py port=fail
... 
omegaconf.errors.ValidationError: Value 'fail' could not be converted to Integer
        full_key: port
        reference_type=Optional[MySQLConfig]
        object_type=MySQLConfig
```

## Duck typing

In the example above `cfg` is duck typed as `MySQLConfig`.
It is actually an instance of `DictConfig`. The duck typing enables static type checking by tools like Mypy or PyCharm.
This reduces development time by catching coding errors before you run your application.

The name [Duck typing](https://en.wikipedia.org/wiki/Duck_typing) comes from the phrase "If it walks like a duck, swims like a duck, and quacks like a duck, then it probably is a duck".
It can be useful when you care about the methods or attributes of an object, not the actual type of the object.

## The ConfigStore
This page introduced the `ConfigStore`, we will see more of it soon.

Let's do a quick dive into the API usage we have seen so far. 
```python
cs = ConfigStore.instance()
cs.store(name="config", node=MySQLConfig)
```
The node parameter is converted to an OmegaConf DictConfig object, the above is equivalent to:
```python
cs.store(name="config", node=OmegaConf.structured(MySQLConfig))
```

You can also pass dictionary, which will similarly be converted to DictConfig:
```python
cs.store(name="config", node={"foo": "bar"})

# equivalent to:
cs.store(name="config", node=OmegaConf.create({"foo": "bar"}))
```
