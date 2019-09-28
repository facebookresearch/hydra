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
Strict mode is a modifier in Hydra's decorator that prevents the introduction of new configuration options through overrides. I.e., strict mode lets you override previously seen options but not adding new ones.
This is useful for catching mistakes in both the command line overrides and in the code early.
Enabling it will change the behavior of the `cfg` object such that:
* Accessing a key that is not in the config will result in a `KeyError` instead of returning `None`
* Attempting to insert a new key will result in a `KeyError` instead of inserting the key

You can learn more about this OmegaConf functionality [here](https://omegaconf.readthedocs.io/en/latest/usage.html#configuration-flags)


Strict mode is on by default when you specify a configuration file for the `config_path` argument in `@hydra.main` decorator. It can be turned on or off (regardless of how `config_path` option in used) via the `strict` argument in your `@hydra.main()` decorator:

```python
@hydra.main(config_path='config.yaml')
def my_app(cfg):
    driver = cfg.db.driver # Okay
    user = cfg.db.user # Okay
    password = cfg.db.password # Not okay, there is no password field in db!
                               # This will result in a KeyError
```

Strict mode will also catch command line override mistakes:
```text
$ python my_app.py db.port=3306
Traceback (most recent call last):
...
KeyError: 'Accessing unknown key in a struct : db.port
```

With strict mode off, the above example will pass successfully:
```python
@hydra.main(config_path='config.yaml', strict=False)
def my_app(cfg):
    cfg.db.port = 3306 # Okay
```
