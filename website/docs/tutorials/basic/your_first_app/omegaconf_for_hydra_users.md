---
id: using_config
title: Using the config object
---

You configuration object is an instance of OmegaConf's DictConfig.  
Here are some of the basic features:

```yaml title="config.yaml"
node:                         # Config is hierarchical
  loompa: 10                  # Simple value
  zippity: ${node.loompa}     # Value interpolation
  do: "oompa ${node.loompa}"  # String interpolation
  waldo: ???                  # Missing value, must be populated prior to access
```

```python title="main.py"
from omegaconf import DictConfig, open_dict, MissingMandatoryValue

@hydra.main(config_name="config")
def my_app(cfg: DictConfig) -> None:
    assert cfg.node.loompa == 10          # attribute style access
    assert cfg["node"]["loompa"] == 10    # dictionary style access
    assert cfg.node.zippity == 10         # Variable interpolation
    assert type(cfg.node.zippity) == int  # Variable interpolation inherits the type
    assert cfg.node.do == "oompa 10"      # string interpolation

    # Accessing a field that is not in the config results in an exception:
    with pytest.raises(AttributeError):
        cfg.new_field = 10

    # you can enable config field addition in a context with open_dict:
    with open_dict(cfg):
        cfg.new_field = 10
    assert cfg.new_field == 10

    # You can check if a field is present in the config:
    assert "new_field" in cfg             # dictionary style
    assert hasattr(cfg, "new_field")      # attribute style

    # Accessing a field marked as missing ('???') raises in an exception
    with pytest.raises(MissingMandatoryValue):
        cfg.node.waldo
 ```
Outputs:
```
$ python my_app.py 
Missing mandatory value: waldo
        full_key: waldo
        reference_type=Optional[Dict[Any, Any]]
        object_type=dict
```
You can learn more about OmegaConf <a class="external" href="https://omegaconf.readthedocs.io/en/latest/usage.html" target="_blank">here</a>.
