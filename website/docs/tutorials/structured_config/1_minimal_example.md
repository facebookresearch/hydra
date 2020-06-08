---
id: minimal_example
title: Minimal example
---

There are four key elements in this example:
- A `@dataclass` describes the application's configuration
- `ConfigStore` manages the Structured Config. 
- `cfg` is `duck typed` as a `MySQLConfig` instead of a `DictConfig`
- There is a subtle typo in the code, can you spot it?

In this example, the config node stored in the `ConfigStore` replaces the traditional `config.yaml` file.  

```python title="my_app_type_error.py" {18}
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
    # pork should be port!
    if cfg.pork == 80:
        print("Is this a webserver?!")

if __name__ == "__main__":
    my_app()
```

### Duck-typing enables static type checking

Duck-typing the config object as `MySQLConfig` enables static type checkers like `mypy` to catch
type errors before you run your code: 
```
$ mypy my_app_type_error.py
my_app_type_error.py:21: error: "MySQLConfig" has no attribute "pork"
Found 1 error in 1 file (checked 1 source file)
```

### Structured Configs enable Hydra to catch type errors at runtime.
If you forget to run `mypy`, Hydra will report the error at runtime:
```
$ python my_app_type_error.py
Key 'pork' not in 'MySQLConfig'
        full_key: pork
        reference_type=Optional[MySQLConfig]
        object_type=MySQLConfig
```

Hydra will also catch typos, or type errors in the command line:
```
$ python my_app_type_error.py port=fail
Error merging override port=fail
Value 'fail' could not be converted to Integer
        full_key: port
        reference_type=Optional[MySQLConfig]
        object_type=MySQLConfig
```
We will see additional types of runtime errors that Hydra can catch later in this tutorial. Such as:
- Trying to read or write a non existent field in your config object
- Assigning a value that is incompatible with the declared type
- Attempting to modify a [frozen config](https://omegaconf.readthedocs.io/en/latest/structured_config.html#frozen)


## Duck typing

In the example above `cfg` is duck typed as `MySQLConfig`.
It is actually an instance of `DictConfig`. The duck typing enables static type checking by tools like Mypy or PyCharm.
This reduces development time by catching coding errors before you run your application.

The name [Duck typing](https://en.wikipedia.org/wiki/Duck_typing) comes from the phrase "If it walks like a duck, swims like a duck, and quacks like a duck, then it probably is a duck".
It can be useful when you care about the methods or attributes of an object, not the actual type of the object.
