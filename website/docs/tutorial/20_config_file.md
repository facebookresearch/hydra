---
id: config_file
title: Configuration file
sidebar_label: Configuration file
---

It can get tedious to type all those command line arguments every time.
Fix it by creating a configuration file:

Configuration file: `config.yaml`
```yaml
db:
  driver: mysql
  user: omry
  pass: secret
```

Specify the config file by passing a `config_path` parameter to the `@hydra.main()` decorator.
The location of the `config_path` is relative to your Python file.

Python file: `my_app.py`
```python
@hydra.main(config_path='config.yaml')
def my_app(cfg):
    print(cfg.pretty())
```

`config.yaml` is loaded automatically when you run your application
```yaml
$ python my_app.py
db:
  driver: mysql
  pass: secret
  user: omry
```

You can override values in the loaded config from the command line:
```yaml
$ python my_app.py db.user=root db.pass=1234
db:
  driver: mysql
  user: root
  pass: 1234
```


### Strict mode
Strict mode is useful for catching mistakes in both the command line overrides and in the code early.
Enabling it will change the behavior of the `cfg` object such that:
* Accessing a key that is not in the config will result in a `KeyError` instead of returning `None`
* Attempting to insert a new key will result in a `KeyError` instead of inserting the key

You can learn more about this OmegaConf functionality [here](https://omegaconf.readthedocs.io/en/latest/usage.html#configuration-flags)

This can be turned on via a `strict=True` argument in your `@hydra.main()` decorator:

```python
@hydra.main(config_path='config.yaml', strict=True)
def my_app(cfg):
    driver = cfg.driver # Okay
    user = cfg.user # Okay
    password = cfg.password # Not okay, there is no password field in db!
                            # This will result in a KeyError
```

Strict mode will also catch command line override mistakes:
```text
$ python my_app.py db.username=root
Traceback (most recent call last):
...
KeyError: 'Accessing unknown key in a struct : db.username'

