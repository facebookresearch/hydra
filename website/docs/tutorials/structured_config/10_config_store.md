---
id: config_store
title: Config Store API
---

Throughout the rest of tutorials, we will be using `ConfigStore` to register dataclasses as input configs in Hydra. 
`ConfigStore` is a singleton storing configs in memory. 
The primary API for interacting with the `ConfigStore` is the store method described below.

### API
```python
class ConfigStore(metaclass=Singleton):
    def store(
        self,
        name: str,
        node: Any,
        group: Optional[str] = None,
        package: Optional[str] = "_group_",
        provider: Optional[str] = None,
    ) -> None:
        """
        Stores a config node into the repository
        :param name: config name
        :param node: config node, can be DictConfig, ListConfig,
            Structured configs and even dict and list
        :param group: config group, subgroup separator is '/',
            for example hydra/launcher
        :param package: Config node parent hierarchy.
            Child separator is '.', for example foo.bar.baz
        :param provider: the name of the module/app providing this config.
            Helps debugging.
        """
    ...
```

### ConfigStore and YAML input configs

`ConfigStore` has feature parity with YAML input configs. On top of that, it also provides typing validation. 
`ConfigStore` can be used alone or together with YAML. We will see more examples later in this series of tutorials. 
For now, let's see how the `ConfigStore` API translates into the YAML input configs, which we've become more familiar 
with after the basic tutorials.

Say we have a simple application and a `db` config group with a `mysql` option:

<div className="row">

<div className="col col--5">

```python title="my_app.py"
@hydra.main(version_base=None, config_path="conf")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
```
</div>
<div className="col  col--4">

```text title="Directory layout"
├─ conf
│  └─ db
│      └─ mysql.yaml
└── my_app.py



```
</div>
<div className="col col--3">

```yaml title="db/mysql.yaml"
driver: mysql
user: omry
password: secret




```
</div>
</div>

What if we want to add an `postgresql` option now? Yes, we can easily add a `db/postgresql.yaml` config group option. But
that is not the only way! We can also use `ConfigStore` to make another config group option for `db` available to Hydra.

To achieve this, we add a few lines (highlighted) in the above `my_app.py` file:


```python title="my_app.py" {1-9}
@dataclass
class PostgresSQLConfig:
    driver: str = "postgresql"
    user: str = "jieru"
    password: str = "secret"

cs = ConfigStore.instance()
# Registering the Config class with the name `postgresql` with the config group `db`
cs.store(name="postgresql", group="db", node=PostgresSQLConfig)

@hydra.main(version_base=None, config_path="conf")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
```


Now that our application has access to both `db` config group options, let's run the application to verify:

<div className="row">

<div className="col col--6">

```commandline title="python my_app.py +db=mysql"
db:
  driver: mysql
  user: omry
  password: secret

```
</div>
<div className="col  col--6">

```commandline title="python my_app.py +db=postgresql"
db:
  driver: postgresql
  user: jieru
  password: secret

```
</div>
</div>


### Example node values
A few examples of supported node values parameters:
```python
from dataclasses import dataclass

from hydra.core.config_store import ConfigStore

@dataclass
class MySQLConfig:
    host: str = "localhost"
    port: int = 3306

cs = ConfigStore.instance()

# Using the type
cs.store(name="config1", node=MySQLConfig)
# Using an instance, overriding some default values
cs.store(name="config2", node=MySQLConfig(host="test.db", port=3307))
# Using a dictionary, forfeiting runtime type safety
cs.store(name="config3", node={"host": "localhost", "port": 3308})
```