---
id: example
title: Minimal example
sidebar_label: Minimal example
---

This is a minimal example of a Hydra app.
Note that the annotated function takes a cfg object as an argument. that cfg object is created and passed in by Hydra.
The configuration is an OmegaConf object, please read about
[OmegaConf](https://omegaconf.readthedocs.io/en/latest/usage.html#access-and-manipulation) to learn how to best use it.

#### minimal.py
```python
import hydra


@hydra.main()
def experiment(cfg):
    print(cfg.pretty())


if __name__ == "__main__":
    experiment()
```

#### Output
By default, Hydra will just pass in an empty configuraiton object:
```yaml
$ python demos/0_minimal/minimal.py
{}
```

You can use the command line interface to pass in arbitrary values, creating an hierarchical configuration object:
```yaml
$ python minimal.py abc=123 hello.a=456 hello.b=5671
abc: 123
hello:
  a: 456
  b: 5671
```


