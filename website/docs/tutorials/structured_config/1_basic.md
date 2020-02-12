---
id: basic
title: Introduction to Structured Configs
sidebar_label: Introduction to Structured Configs
---
This is an advanced tutorial that assumes that you are comfortable with the concepts introduced in the [Basic Tutorial](/tutorials/basic/1_simple_cli_app.md).

Structured configs are new in **Hydra 1.0.0**. The key idea is that a regular Python dataclass or object can be used to construct a DictConfig object.
The DictConfig object is very similar to those defined through config files, with one important difference:
Structured configs are strongly typed.

This enables two new features:

 * **Static type checking**: The resulting object looks much like an instance of the underlying type. You can annotate the config object as the type and use Mypy or other static
type checkers to perform static type analysis on your config objects.
* **Runtime type checking**: The type information in retained at runtime and is used to validate that changes to your object are conforming to underlying type specification. 
This is especially useful for catching type errors during the composition of your configuration.
  
You don't need a deep understanding of structured configs for this tutorial. Visit the <a class="external" href="https://omegaconf.readthedocs.io/en/latest/structured_config.html" target="_blank">documentation</a> later to learn more.

<div class="alert alert--info" role="alert">
<strong>NOTE</strong>: 
Structured configs are a new feature with significant surface area. Please report any difficulties or issues you are running into.
</div>
<br/>
<div class="alert alert--info" role="alert">
<strong>NOTE</strong>: 
This is an experimental feature and API and behavior may change in a future version.
</div>
<br/>

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

# You can also register objects of this class, allowing easy overriding of default values.
# If you are registering 'config' more than once the last one will replace the previous ones.
cfg_store.store(node=MySQLConfig(user="root", password="1234"), name="config")


# The real type of cfg is actually DictConfig, but we lie a little to get static type checking.
# If it swims like a duck and quacks like a duck...
@hydra.main(config_name="config")
def my_app(cfg: MySQLConfig) -> None:
    print(
        f"Connecting to {cfg.driver} at {cfg.host}:{cfg.port}, user={cfg.user}, password={cfg.password}"
    )


if __name__ == "__main__":
    my_app()
```

In addition to the static type checking, You also get runtime type checking.
For example, overriding the port to something that cannot be converted to an integer will result in a ValidationError.

```python
$ python my_app.py port=fail
Traceback (most recent call last):
...
omegaconf.errors.ValidationError: Error setting 'port = fail' : Value 'fail' could not be converted to Integer
```