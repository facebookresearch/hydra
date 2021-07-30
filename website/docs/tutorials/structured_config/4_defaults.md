---
id: defaults
title: Defaults List
---

import {ExampleGithubLink} from "@site/src/components/GithubLink"

<ExampleGithubLink to="examples/tutorials/structured_configs/4_defaults/my_app.py"/>

You can define a defaults list in your primary Structured Config just like you can in your primary `config.yaml` file.
The example below extends the previous example by adding a defaults list that will load `db=mysql` by default.

<div class="alert alert--info" role="alert">
NOTE: You can still place your defaults list in your primary (YAML) config file (Example in next page).
</div><br/>

```python {11-14,19,25}
from omegaconf import MISSING, OmegaConf

@dataclass
class MySQLConfig:
    ...

@dataclass
class PostGreSQLConfig:
    ...

defaults = [
    # Load the config "mysql" from the config group "db"
    {"db": "mysql"}
]

@dataclass
class Config:
    # this is unfortunately verbose due to @dataclass limitations
    defaults: List[Any] = field(default_factory=lambda: defaults)

    # Hydra will populate this field based on the defaults list
    db: Any = MISSING

cs = ConfigStore.instance()
cs.store(group="db", name="mysql", node=MySQLConfig)
cs.store(group="db", name="postgresql", node=PostGreSQLConfig)
cs.store(name="config", node=Config)


@hydra.main(config_path=None, config_name="config")
def my_app(cfg: Config) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
```
Running `my_app.py` loads the mysql config option by default:
```yaml
$ python my_app.py
db:
  driver: mysql
  ...
```

You can override the default option via the command line:
```yaml
$ python my_app.py db=postgresql
db:
  driver: postgresql
  ...
```

#### Requiring users to specify a default list value

Set `db` as `MISSING` to require the user to specify a value on the command line.

<div className="row">
<div className="col col--6">

```python title="Defaults list with a missing db"
defaults = [
    {"db": MISSING}
]


```

</div>

<div className="col  col--6">

```text title="Output"
$ python my_app.py
You must specify 'db', e.g, db=<OPTION>
Available options:
        mysql
        postgresql
```

</div>
</div>

#### Merge order for combining a defaults list with other structured config fields

Just like with defaults lists in `yaml` files, the `_self_` keyword can be used
in a defaults list that is part of a structured config.
Using `_self_` in a structured config's defaults list gives explicit control
over the order in which the structured config's fields are merged with the
configs from the defaults list
(see [Compositon Order](advanced/defaults_list.md#composition-order)).