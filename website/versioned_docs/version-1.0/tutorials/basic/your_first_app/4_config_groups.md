---
id: config_groups
title: Grouping config files
---

[![Example](https://img.shields.io/badge/-Example-informational)](https://github.com/facebookresearch/hydra/tree/master/examples/tutorials/basic/your_first_hydra_app/4_config_groups)

Suppose you want to benchmark your application on each of PostgreSQL and MySQL. To do this, use config groups. 

A _**Config Group**_ is a named group with a set of valid options.

* The config options are mutually exclusive. Only one can be selected.
* Selecting a non-existent config option generates an error message with the valid options.

To create a config group, create a directory. e.g. `db` to hold a file for each database configuration option. 
Since we are expecting to have multiple config groups, we will proactively move all the configuration files 
into a `conf` directory.


``` text title="Directory layout"
├── conf
│   └── db
│       ├── mysql.yaml
│       └── postgresql.yaml
└── my_app.py
```

```yaml title="db/mysql.yaml"
# @package _group_
driver: mysql
user: omry
password: secret
```
The config group determines the `package` of the config content inside the final config object.  
```yaml title="Interpretation of db/mysql.yaml" {1}
db:
  driver: mysql
  user: omry
  password: secret 
```
In Hydra 1.1 `_group_` will become the default package.  
For now, add `# @package _group_` at the top of your config group files.  
Learn more about packages directive [here](/advanced/overriding_packages.md). 

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

You can append an item a config group to the `Defaults List`.  
The `Defaults List` is described on the next page.
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

### More advanced usages of config groups
Config groups can be nested. For example the config group `db/mysql/storage_engine` can contain `innodb.yaml` and `myisam.yaml`.
When selecting an option from a nested config group, use `/`:
```
$ python my_app.py +db=mysql +db/mysql/storage_engine=innodb
db:
  driver: mysql
  user: omry
  password: secret 
  mysql:
    storage_engine:
      innodb_data_file_path: /var/lib/mysql/ibdata1
      max_file_size: 1G
```

This simple example also demonstrated a very powerful feature of Hydra:
You can compose your configuration object from multiple configuration groups.


