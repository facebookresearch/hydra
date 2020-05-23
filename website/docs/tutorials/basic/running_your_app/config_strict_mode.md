---
id: strict_mode
title: Strict config errors
---


### Overview
Hydra sets the `struct` flag on the config object. This catches references to fields not specified in the config. 

This results in two useful behaviors:

- Accessing a field that not in the config file raises exception:
```python {3}
@hydra.main(config_name='config')
def my_app(cfg : DictConfig) -> None:
    print(cfg.db.drover)  # typo: cfg.db.driver, raises an exception
```

- Overriding a field that is not in the config file via the command line prints an error:
```text {1}
$ python my_app.py db.drover=mariadb
Error merging overrides
Key 'drover' in not in struct
        full_key: db.drover
        reference_type=Optional[Dict[Any, Any]]
        object_type=dict
```

### Adding fields at runtime
- You can disable the struct flag a specific context using `open_dict`.
- You can disable the struct flag permanently for your config using `OmegaConf.set_struct(cfg, False)`.

Learn more about OmegaConf struct flag <a class="external" href="https://omegaconf.readthedocs.io/en/latest/usage.html#struct-flag" target="_blank">here</a>.
