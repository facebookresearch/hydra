---
id: simple_cli
title: Simple command line application
sidebar_label: Simple command line application
---

This is a simple Hydra application that prints your configuration.
The `my_app` function is a place holder for your code.
We will slowly evolve this example to showcase more Hydra features.

The examples in this tutorial are available [here](https://github.com/facebookresearch/hydra/tree/master/examples/tutorial).

Python file: `my_app.py`
```python
from omegaconf import DictConfig
import hydra

@hydra.main()
def my_app(cfg: DictConfig) -> None:
    print(cfg.pretty())

if __name__ == "__main__":
    my_app()
```
Hydra creates the `cfg` object and pass it to the function annotated with `@hydra.main`.
`DictConfig` is a part of <a class="external" href="https://omegaconf.readthedocs.io/en/latest/usage.html#access-and-manipulation" target="_blank">OmegaConf</a>.
You don't need a deep understanding of OmegaConf for this tutorial, but I recommend reading the docs later.

You can pass arbitrary command line arguments from which Hydra will create a hierarchical configuration object:
```yaml
$ python my_app.py db.driver=mysql db.user=omry db.pass=secret
db:
  driver: mysql
  pass: secret
  user: omry
```
