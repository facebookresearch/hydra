---
id: basic
title: Introduction to Structured Configs
sidebar_label: Introduction to Structured Configs
---
This is an advanced tutorial that assumes that you are comfortable with the concepts introduced in the [Basic Tutorial](/tutorials/basic/1_simple_cli_app.md).

Structured Configs are new in **Hydra 1.0.0**. The key idea is that a regular Python dataclass or instance can be used to define the configuration.
The DictConfig object is very similar to those defined through config files, with one important difference:
Structured Configs are strongly typed.

This enables two new features:

 * **Static type checking**: The resulting object looks much like an instance of the underlying type. You can annotate the config object as the type and use Mypy or other static
type checkers to perform static type analysis on your config objects.
* **Runtime type checking**: The type information in retained at runtime and is used to validate that changes to your object are conforming to underlying type specification. 
This is especially useful for catching type errors during the composition of your configuration.

Structured Configs support primitive types, Enums, nesting of other Structured Configs and typed containers like `List` or `Dict`.
This tutorial does not assume complete knowledge of Structured Configs. Visit the <a class="external" href="https://omegaconf.readthedocs.io/en/latest/structured_config.html" target="_blank">documentation</a> later to learn more.

<div class="alert alert--info" role="alert">
1. The APIs and behaviors described in this tutorial are experimental and may change in a future version<br/> 
2. Structured Configs adds a significant API surface area. Please report any issues
</div>
<br/>

This tutorial follows a path similar to that of the Basic Tutorial, but with Structured Configs instead of configuration files.
The [Structured config as schema](/tutorials/structured_config/6_schema.md) page shows how use Structured configs as a schema to validate configuration files.

#### Minimal example
Below is a minimal example that registers a structured config in the ConfigStore under the name "config", 
and proceeds to use it as the primary config of the application.

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


cfg_store = ConfigStore.instance()
# Registering the Config class with the name 'config'
cfg_store.store(node=MySQLConfig, name="config")

@hydra.main(config_name="config")
def my_app(cfg: MySQLConfig) -> None:
    # The real type of cfg is DictConfig, but we lie a little to get static type checking.
    # If it swims like a duck and quacks like a duck, it's a "duck".
    print(
        f"Connecting to {cfg.driver} at {cfg.host}:{cfg.port}, user={cfg.user}, password={cfg.password}"
    )


if __name__ == "__main__":
    my_app()
```

You can also register instances of the dataclasses, allowing easy overriding of default values.
If you are registering 'config' more than once the last one will replace the previous ones.
```python
cfg_store.store(node=MySQLConfig(user="root", password="1234"), name="config")
```


Running this app you would see the expected output:
```text
$ python my_app.py 
Connecting to mysql at localhost:3306, user=root, password=1234
```

In addition to the static type checking, You also get runtime type checking.
For example, overriding the port to something that cannot be converted to an integer will result in a ValidationError.

```python
$ python my_app.py port=fail
Traceback (most recent call last):
...
omegaconf.errors.ValidationError: Error setting 'port = fail' : Value 'fail' could not be converted to Integer
```
