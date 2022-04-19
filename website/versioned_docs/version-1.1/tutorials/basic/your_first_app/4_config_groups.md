---
id: config_groups
title: Grouping config files
---

import {ExampleGithubLink} from "@site/src/components/GithubLink"

<ExampleGithubLink to="examples/tutorials/basic/your_first_hydra_app/4_config_groups"/>

Suppose you want to benchmark your application on each of PostgreSQL and MySQL. To do this, use config groups. 

A _**Config Group**_ is a named group with a set of valid options.
Selecting a non-existent config option generates an error message with the valid options.

### Creating config groups
To create a config group, create a directory. e.g. `db` to hold a file for each database configuration option. 
Since we are expecting to have multiple config groups, we will proactively move all the configuration files 
into a `conf` directory.

<div className="row">
<div className="col col--4">

``` text title="Directory layout"
├─ conf
│  └─ db
│      ├─ mysql.yaml
│      └─ postgresql.yaml
└── my_app.py
```
</div>

<div className="col col--4">

```yaml title="db/mysql.yaml"
driver: mysql
user: omry
password: secret


```
</div><div className="col col--4">

```yaml title="db/postgresql.yaml"
driver: postgresql
user: postgres_user
password: drowssap
timeout: 10

```

</div>
</div>

### Using config groups
Since we moved all the configs into the `conf` directory, we need to tell Hydra where to find them using the `config_path` parameter.
**`config_path` is a directory relative to `my_app.py`**.
```python title="my_app.py" {4}
from omegaconf import DictConfig, OmegaConf
import hydra

@hydra.main(config_path="conf")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()
```

Running `my_app.py` without requesting a configuration will print an empty config.
```yaml
$ python my_app.py
{}
```

Select an item from a config group with `+GROUP=OPTION`, e.g: 
```yaml {2}
$ python my_app.py +db=postgresql
db:
  driver: postgresql
  pass: drowssap
  timeout: 10
  user: postgres_user
```

By default, the config group determines where the config content is placed inside the final config object. 
In Hydra, the path to the config content is referred to as the config `package`. 
The package of `db/postgresql.yaml` is `db`:


Like before, you can still override individual values in the resulting config:
```yaml
$ python my_app.py +db=postgresql db.timeout=20
db:
  driver: postgresql
  pass: drowssap
  timeout: 20
  user: postgres_user
```

### Advanced topics
 - Config content can be relocated via package overrides. See [Reference Manual/Packages](advanced/overriding_packages.md).    
 - Multiple options can be selected from the same Config Group by specifying them as a list.  
   See [Common Patterns/Selecting multiple configs from a Config Group](patterns/select_multiple_configs_from_config_group.md)  


