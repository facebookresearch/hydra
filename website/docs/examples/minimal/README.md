---
id: example
title: Minimal example
sidebar_label: Minimal
---
## Minimal example

```python
import hydra


@hydra.main()
def experiment(cfg):
    print(cfg.pretty())


if __name__ == "__main__":
    experiment()
```

Hydra will construct the configuration object for you, in this example there is no input to construct it from, so it's empty.
```yaml
$ python demos/0_minimal/minimal.py
{}
```

You can pass in arbitrary configuration from the command line and it will be converted to a tree
structure:
```yaml
$ python demos/0_minimal/minimal.py abc=123 hello.a=456 hello.b=5671
abc: 123
hello:
  a: 456
  b: 5671
```

The cfg argument passed into experiment() is an OmegaConf object, please read about [OmegaConf](https://omegaconf.readthedocs.io/en/latest/usage.html#access-and-manipulation) to learn how to best use it.

