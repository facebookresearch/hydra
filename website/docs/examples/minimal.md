---
id: minimal
title: Minimal example
sidebar_label: Minimal example
---

This is a minimal example of a Hydra app.
The experiment() function is a place holder for your actual code.
we will evolve this example slowly to show-case more Hydra features.
Note that the annotated function takes a `cfg` argument. This `cfg` is an OmegaConf object created and passed in by Hydra.
Please read about [OmegaConf](https://omegaconf.readthedocs.io/en/latest/usage.html#access-and-manipulation) to learn how to best use it.

### minimal.py
```python
import hydra


@hydra.main()
def experiment(cfg):
    print(cfg.pretty())


if __name__ == "__main__":
    experiment()
```

### Output
By default, Hydra will just pass in an empty configuration object:
```yaml
$ python experiment.py
{}
```

You can use the command line interface to pass in arbitrary values, creating a hierarchical configuration object:
```yaml
$ python minimal.py abc=123 hello.a=456 hello.b=5671
abc: 123
hello:
  a: 456
  b: 5671
```

Check the [runnable example](https://github.com/facebookresearch/hydra/blob/master/demos/0_minimal/minimal.py).
