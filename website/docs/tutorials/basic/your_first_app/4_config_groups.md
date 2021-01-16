---
id: config_groups
title: Grouping config files
---

[![Example](https://img.shields.io/badge/-Example-informational)](https://github.com/facebookresearch/hydra/tree/master/examples/tutorials/basic/your_first_hydra_app/4_config_groups)

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
user: postgre_user
password: drowssap
timeout: 10

```

</div>
</div>

### Using config groups
Since we moved all the configs into the `conf` directory, we need to tell Hydra where to find them using the `config_path` parameter.
**`config_path` is a directory relative to `my_app.py`**.
```python title="my_app.py" {1}
@hydra.main(config_path="conf")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
```

Running `my_app.py` without requesting a configuration will print an empty config.
```yaml
$ python my_app.py
{}
```

Select an item from the defaults list with **+GROUP=OPTION**, e.g: 
```yaml
$ python my_app.py +db=postgresql
db:
  driver: postgresql
  pass: drowssap
  timeout: 10
  user: postgre_user
```

Like before, you can still override individual values in the resulting config:
```yaml
$ python my_app.py +db=postgresql db.timeout=20
db:
  driver: postgresql
  pass: drowssap
  timeout: 20
  user: postgre_user
```

By default, the config group determines the `package` of the config content inside the final config object.
The package of `db/mysql.yaml` is `db`:
```yaml title="Interpretation of db/mysql.yaml" {1}
db:
  driver: mysql
  user: omry
  password: secret 
```

:::info Advanced
Config content can be relocated via package overrides.  
This is an advanced topic covered in [Reference Manual/Packages](advanced/overriding_packages.md).
:::


### More advanced usages of config groups
Config groups can be nested. For example the config group `db/mysql/engine` can contain `innodb.yaml` and `myisam.yaml`.
When selecting an option from a nested config group, use `/`:
```
$ python my_app.py +db=mysql +db/mysql/engine=innodb
db:
  driver: mysql
  user: omry
  password: secret 
  mysql:
    engine:
      innodb_data_file_path: /var/lib/mysql/ibdata1
      max_file_size: 1G
```

This simple example also demonstrated a very powerful feature of Hydra:
You can compose your configuration object from multiple configuration groups.

:::info Advanced
You can select multiple options from the same Config Group by specifying them as a list.  
This is an advanced topic covered in [Common Patterns/Selecting multiple configs from a Config Group](patterns/select_multiple_configs_from_config_group.md).
:::


