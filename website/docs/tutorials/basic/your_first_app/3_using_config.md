---
id: using_config
title: Using the config object
---

import {ExampleGithubLink} from "@site/src/components/GithubLink"

<ExampleGithubLink to="examples/tutorials/basic/your_first_hydra_app/3_using_config"/>

Here are some basic features of the Hydra Configuration Object:

```yaml title="config.yaml"
node:                         # Config is hierarchical
  loompa: 10                  # Simple value
  zippity: ${node.loompa}     # Value interpolation
  do: "oompa ${node.loompa}"  # String interpolation
  waldo: ???                  # Missing value, must be populated prior to access
```

```python title="main.py"
@hydra.main(config_name="config")
def my_app(cfg: DictConfig):
    assert cfg.node.loompa == 10          # attribute style access
    assert cfg["node"]["loompa"] == 10    # dictionary style access

    assert cfg.node.zippity == 10         # Value interpolation
    assert isinstance(cfg.node.zippity, int)  # Value interpolation type
    assert cfg.node.do == "oompa 10"      # string interpolation

    cfg.node.waldo                        # raises an exception
 ```
Outputs:
```
$ python my_app.py 
Missing mandatory value: waldo
        full_key: waldo
        reference_type=Optional[Dict[Any, Any]]
        object_type=dict
```

Hydra's configuration object is an instance of OmegaConf's DictConfig.
You can learn more about OmegaConf <a class="external" href="https://omegaconf.readthedocs.io/en/latest/usage.html#access-and-manipulation" target="_blank">here</a>.
