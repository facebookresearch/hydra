---
id: minimal
title: Minimal example
sidebar_label: Minimal example
---

This is a minimal example of a Hydra app.
The experiment() function is a place holder for your actual code.
We will slowly evolve this example to show-case more Hydra features.

### minimal.py
```python
import hydra


@hydra.main()
def experiment(cfg):
    print(cfg.pretty())


if __name__ == "__main__":
    experiment()
```
Note that the function takes an `cfg` object that holds the configuration for your function.

Initially we will command line interface to pass in arbitrary values, creating a hierarchical configuration 
object:
```yaml
$ python minimal.py abc=123 hello.a=456 hello.b=5671
abc: 123
hello:
  a: 456
  b: 5671
```

The `cfg` is a [OmegaConf](https://omegaconf.readthedocs.io/en/latest/usage.html#access-and-manipulation) 
object


Check the [runnable example](https://github.com/facebookresearch/hydra/blob/master/demos/0_minimal/minimal.py).
