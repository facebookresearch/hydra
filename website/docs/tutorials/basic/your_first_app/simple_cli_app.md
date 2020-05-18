---
id: simple_cli
title: A simple command line app
---

This is a simple Hydra application that prints your configuration.
The `my_app` function is a place holder for your code.
We will slowly evolve this example to showcase more Hydra features.

The examples in this tutorial are available [here](https://github.com/facebookresearch/hydra/tree/master/examples/tutorials/basic).

```python title="my_app.py"
from omegaconf import DictConfig
import hydra

@hydra.main()
def my_app(cfg: DictConfig) -> None:
    print(cfg.pretty())

if __name__ == "__main__":
    my_app()
```
In this example, Hydra creates an empty `cfg` object and pass it to the function annotated with `@hydra.main`.

You can pass command line arguments from which Hydra creates a hierarchical configuration object:
```yaml
$ python my_app.py db.driver=mysql db.user=omry db.pass=secret
db:
  driver: mysql
  pass: secret
  user: omry
```
