---
id: simple_cli
title: A simple command-line application
---

[![Example](https://img.shields.io/badge/-Example-informational)](https://github.com/facebookresearch/hydra/blob/master/examples/tutorials/basic/your_first_hydra_app/1_simple_cli/my_app.py)

This is a simple Hydra application that prints your configuration.
The `my_app` function is a place holder for your code.
We will slowly evolve this example to showcase more Hydra features.

The examples in this tutorial are available [here](https://github.com/facebookresearch/hydra/tree/master/examples/tutorials/basic).

```python title="my_app.py"
from omegaconf import DictConfig, OmegaConf
import hydra

@hydra.main()
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

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

See [Hydra's command line flags](advanced/hydra-command-line-flags.md) and
[Basic Override Syntax](advanced/override_grammar/basic.md) for more information about the command line.
