---
id: defaults
title: Defaults
sidebar_label: Defaults
---
Eventually you decide that you want to use MySQL by default and you no longer want to type `db=mysql` every time you run
your application.

You can add a `defaults` list into your config file:
The list order determines the order of composition.

Configuration file (`config.yaml`):
```yaml
defaults:
    - db: mysql
```

Remember to specify this file in the `config_path`:
```python
@hydra.main(config_path='conf/config.yaml')
def my_app(cfg):
    print(cfg.pretty())
```

When you run the updated application, MySQL is loaded by default:
```yaml
$ python my_app.py
db:
  driver: mysql
  pass: secret
  user: omry
```

But you can still load PostgreSQL, and override individual values:
```yaml
$ python my_app.py db=postgresql db.timeout=20
db:
  driver: postgresql
  pass: drowssap
  timeout: 20
  user: postgre_user
```

### Not loading a default
You can prevent a default from being loaded by assigning `null` to it in the command line:
```yaml
$ python my_app.py db=null
{}
```

### Merging a standalone config file
Sometimes a config file you want to merge does not belong in any group.
The following will load `some_file.yaml` from your config directory:
```yaml
defaults:
    - some_file
```

Note that `some_file` is hard coded in the config and you cannot influence its loading.
In most cases, you actually want to have a config group like `db`.
