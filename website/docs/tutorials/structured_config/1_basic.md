---
id: basic
title: Introduction to Structured Configs
sidebar_label: Introduction to Structured Configs
---
This is an advanced tutorial that assumes that you are comfortable with the concepts introduced in the [Basic Tutorial](/tutorials/basic/1_simple_cli_app.md).

Structured configs are classes that are used to define your config, enabling two primary features:

* **Static type checking**: A config object looks much like an instance of the underlying type, you can annotate it as that type and use Mypy or other static
type checkers to perform static type analysis on it.
* **Runtime type checking**: The type information in retained at runtime and is used to validate that changes to your object conforms to the underlying type specification. 
This is especially useful for catching type errors during the composition of your configuration.

Structured Configs are new in **Hydra 1.0.0**. The key idea is that you can use regular Python dataclasses to describe your configuration structure and types.
The configuration objects created from Structured Configs uses the type information for validating the composition and other mutations of the config.

### Structured Configs major features

Some of the major features Structured Configs supports are:
- Primitive types (int, bool, float, str, Enums) 
- Nesting of structured configs
- Containers (List and Dict) containing primitives or Structured Configs.
- Optional fields

#### Structured Configs Limitations
- `Union` types are not supported (except `Optional`)
- User methods are not supported.

### Overview

There are two primary ways for using Structured configs.
- In place of configuration files
- As a [schema](/tutorials/structured_config/6_schema.md) validating configuration files

With both methods, you get everything else Hydra has to offer (Config composition, Command line overrides etc).
This tutorial covers both methods, read it in order.

This tutorial does not require a complete knowledge of Structured Configs. You can visit the <a class="external" href="https://omegaconf.readthedocs.io/en/latest/structured_config.html" target="_blank">OmegaConf Structured Configs page</a> to learn more later.

<div class="alert alert--info" role="alert">
1. The APIs and behaviors described in this tutorial are experimental and may change in a future version<br/> 
2. Structured configs are new, please report any issues<br/>
</div>
<br/>

#### Minimal example
This tutorial uses the `ConfigStore`, an in-memory Singleton that stores configurations.

The following example uses a `@dataclass` as the description of the application's configuration. 
As usual, `cfg` is an instance of `DictConfig`; declaring it's type as `MySQLConfig` enables static type checking by tools like Mypy or PyCharm.

```python
from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore

@dataclass
class MySQLConfig:
    driver: str = "mysql"
    host: str = "localhost"
    port: int = 3306
    user: str = "omry"
    password: str = "secret"

# Register MySQLConfig class as 'config'
cs = ConfigStore.instance()
cs.store(name="config", node=MySQLConfig)

@hydra.main(config_name="config")
def my_app(cfg: MySQLConfig) -> None:
    # The real type of cfg is DictConfig, but we lie a little to get static type checking.
    # If it swims like a duck and quacks like a duck, it's a duck.
    print(
        f"Connecting to {cfg.driver} at {cfg.host}:{cfg.port}, user={cfg.user}, password={cfg.password}"
    )


if __name__ == "__main__":
    my_app()
```

You can still override values in the config from the command line:
```text
$ python my_app.py user=bond
Connecting to mysql at localhost:3306, user=bond, password=1234
```

In addition to the static type checking, You also get runtime type checking.
```python
$ python my_app.py port=fail
Traceback (most recent call last):
...
omegaconf.errors.ValidationError: Error setting 'port = fail' : Value 'fail' could not be converted to Integer
```

#### Overriding default values in the `@dataclass`
You can use instances of the dataclasses to override default values in the stored config.
```python
cs.store(name="config", node=MySQLConfig(user="root", password="1234"))
```
If you register more than one config with the same name the last one will replace the previous ones.