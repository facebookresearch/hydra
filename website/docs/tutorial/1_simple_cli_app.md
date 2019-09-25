---
id: simple_cli
title: Simple command line application
sidebar_label: Simple command line application
---

A very small Hydra application looks like this:

### my_app.py
```python
import hydra

@hydra.main()
def my_app(cfg):
    print(cfg.pretty())

if __name__ == "__main__":
    my_app()
```
Note that the function takes a `cfg` object that holds the configuration for your function.

Initially we will command line interface to pass in arbitrary values, creating a hierarchical configuration 
object:
```yaml
$ python my_app.py db.driver=mysql db.user=omry db.pass=secret
db:
  driver: mysql
  pass: secret
  user: omry
```

The `cfg` is an [OmegaConf](https://omegaconf.readthedocs.io/en/latest/usage.html#access-and-manipulation) 
object
