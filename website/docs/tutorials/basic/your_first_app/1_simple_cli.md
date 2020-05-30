---
id: simple_cli
title: A simple command-line application
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

You can add config values via the command line. The `+` indicates that the field is new.

```yaml
$ python my_app.py +db.driver=mysql +db.user=omry +db.password=secret
db:
  driver: mysql
  user: omry
  password: secret
```

