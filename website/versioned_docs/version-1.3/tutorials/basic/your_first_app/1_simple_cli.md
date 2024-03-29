---
id: simple_cli
title: A simple command-line application
---

import GithubLink,{ExampleGithubLink} from "@site/src/components/GithubLink"

<ExampleGithubLink to="examples/tutorials/basic/your_first_hydra_app/1_simple_cli/my_app.py"/>

This is a simple Hydra application that prints your configuration.
The `my_app` function is a placeholder for your code.
We will slowly evolve this example to showcase more Hydra features.

The examples in this tutorial are available <GithubLink to="examples/tutorials/basic">here</GithubLink>.

```python title="my_app.py"
from omegaconf import DictConfig, OmegaConf
import hydra

@hydra.main(version_base=None)
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()
```
In this example, Hydra creates an empty `cfg` object and passes it to the function annotated with `@hydra.main`.

You can add config values via the command line. The `+` indicates that the field is new.

```yaml
$ python my_app.py +db.driver=mysql +db.user=omry +db.password=secret
db:
  driver: mysql
  user: omry
  password: secret
```

:::info
See the [version_base page](../../../upgrades/version_base.md) for details on the version_base parameter.
:::

See [Hydra's command line flags](advanced/hydra-command-line-flags.md) and
[Basic Override Syntax](advanced/override_grammar/basic.md) for more information about the command line.
