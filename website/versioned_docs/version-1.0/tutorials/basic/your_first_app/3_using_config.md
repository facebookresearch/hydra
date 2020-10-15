---
id: using_config
title: Using the config object
---

[![Example](https://img.shields.io/badge/-Example-informational)](https://github.com/facebookresearch/hydra/tree/master/examples/tutorials/basic/your_first_hydra_app/3_using_config)

You configuration object is an instance of OmegaConf's DictConfig.  
Here are some of the basic features:

```yaml title="config.yaml"
node:                         # Config is hierarchical
  loompa: 10                  # Simple value
  zippity: ${node.loompa}     # Value interpolation
  do: "oompa ${node.loompa}"  # String interpolation
  waldo: ???                  # Missing value, must be populated prior to access
```

```python title="my_app.py"
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
You can learn more about OmegaConf <a class="external" href="https://omegaconf.readthedocs.io/en/latest/usage.html#access-and-manipulation" target="_blank">here</a>.
