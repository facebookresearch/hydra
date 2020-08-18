---
id: defaults
title: Defaults
sidebar_label: Defaults
---

After office politics, you decide that you want to use MySQL by default.
You no longer want to type `db=mysql` every time you run your application.

You can add a `defaults` list into your config file.

## Config group defaults

Configuration file: `config.yaml`
```yaml
defaults:
  - db: mysql
```

Remember to specify `config.yaml` as the `config_path`.
```python
@hydra.main(config_path='conf/config.yaml')
def my_app(cfg):
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

You can prevent a default from being loaded by assigning `null` to it in the command line:
```yaml
$ python my_app.py db=null
{}
```

## Non-config group defaults
Sometimes a config file you want to merge does not belong in any config group.
The following will load `some_file.yaml` from your config directory:
```yaml
defaults:
  - some_file
```
Config files that not a part of a `config group` like `db` cannot be overridden.
