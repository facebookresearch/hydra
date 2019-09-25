---
id: simple_cli
title: Simple command line application
sidebar_label: Simple command line application
---

This is a simple Hydra application. The `my_app` function is a place holder 
for your code. We will slowly evolve this example to show-case more Hydra features.

Python file (`my_app.py`):
```python
import hydra

@hydra.main()
def my_app(cfg):
    print(cfg.pretty())

if __name__ == "__main__":
    my_app()
```
Note that the function takes a `cfg` object that holds the configuration for your function.

We can pass arbitrary command line arguments, which will be used to create a hierarchical configuration object:
```yaml
$ python my_app.py db.driver=mysql db.user=omry db.pass=secret
db:
  driver: mysql
  pass: secret
  user: omry
```

The `cfg` is an [OmegaConf](https://omegaconf.readthedocs.io/en/latest/usage.html#access-and-manipulation) 
object
