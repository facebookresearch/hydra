---
id: defaults
title: Selecting defaults for config groups
---

[![Example](https://img.shields.io/badge/-Example-informational)](https://github.com/facebookresearch/hydra/tree/master/examples/tutorials/basic/your_first_hydra_app/5_defaults)

After office politics, you decide that you want to use MySQL by default.
You no longer want to type `+db=mysql` every time you run your application.

You can add a `defaults` list into your config file.

This tutorial page briefly describes the Defaults List.  
Refer to [The Defaults List page](../../../advanced/defaults_list) for more information.

## Config group defaults

```yaml title="config.yaml"
defaults:
  - db: mysql
```

Remember to specify the `config_name`:
```python
@hydra.main(config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
```

When you run the updated application, MySQL is loaded by default.
```yaml
$ python my_app.py
db:
  driver: mysql
  pass: secret
  user: omry
```

You can have multiple items in the defaults list, e.g
```yaml
defaults:
 - db: mysql
 - db/mysql/storage_engine: innodb
```

The defaults are ordered:
 * If multiple configs define the same value, the last one wins. 
 * If multiple configs contribute to the same dictionary, the result is the combined dictionary.


### Overriding a config group default

You can still load PostgreSQL, and override individual values.
```yaml
$ python my_app.py db=postgresql db.timeout=20
db:
  driver: postgresql
  pass: drowssap
  timeout: 20
  user: postgre_user
```

You can remove a default entry from the defaults list by prefixing it with ~:
```yaml
$ python my_app.py ~db
{}
```

## Non-config group defaults
Sometimes a config file does not belong in any config group.
You can still load it by default. Here is an example for `some_file.yaml`.
```yaml
defaults:
  - some_file
```
Config files that are not part of a config group will always be loaded. They cannot be overridden.  
Prefer using a config group.
