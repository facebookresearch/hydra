---
id: config_file
title: Configuration file
sidebar_label: Configuration file
---

After a while it gets annoying to type all those command line flags every time.
Fix it by creating a configuration file:

### Configuration file
Configuration file (`config.yaml`):
```yaml
db:
  driver: mysql
  user: omry
  pass: secret
```

You can pass in a config file for your app by specifying a config_path parameter to the `@hydra.main()` decoration.
The location of the `config_path` is relative to your python file.

Python file (`my_app.py`):
```python
import hydra

@hydra.main(config_path='config.yaml')
def my_app(cfg):
    print(cfg.pretty())

if __name__ == "__main__":
    my_app()
```

`config.yaml` gets loaded automatically when you run the app.
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
Enabling strict mode will change the behavior of the `cfg` object in the following way:
* Reading a key that is not there will result in a KeyError instead of returning None
* Writing key that is not there would result in a KeyError instead of inserting the key
This effects also command line overrides.

This is useful for catching mistakes in the code or in the command line earlier.

You can learn more about this OmegaConf functionality [here](https://omegaconf.readthedocs.io/en/latest/usage.html#configuration-flags)

This can be turned on via a `strict=True` in your hydra.main decorator:

```python
@hydra.main(config_path='config.yaml', strict=True)
def my_app(cfg):
    print(cfg.pretty())
    driver = cfg.driver # Okay
    user = cfg.user # Okay
    password = cfg.password # Not okay, there is no password field in db!
                            # This will result in a KeyError
```

Strict mode will also catch mistakes in the overriding of values in the config:
```text
$ python my_app.py db.username=root
Traceback (most recent call last):
...
KeyError: 'Accessing unknown key in a struct : db.username'

