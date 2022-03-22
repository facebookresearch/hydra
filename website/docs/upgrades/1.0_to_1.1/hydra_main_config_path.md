---
id: changes_to_hydra_main_config_path
title: Changes to @hydra.main() and hydra.initialize()
---

Prior to Hydra 1.1, **@hydra.main()** and **hydra.initialize()** default `config path` was the directory containing the Python app (calling **@hydra.main()** or **hydra.initialize()**).

This can cause unexpected behavior:
- Sibling directories are interpreted as config groups, which can lead to surprising results (See [#1533](https://github.com/facebookresearch/hydra/issues/1533)).
- The subtree added automatically can have many files/directories - which will cause **--help** to be very slow as it's scanning for all config groups/config files (See [#759](https://github.com/facebookresearch/hydra/issues/759)).

To address these issues, Hydra 1.1 issues a warning if the config_path is not specified.  
Your options are as follows:

### Dedicated config directory
For applications with config files, specify a directory like "conf" to use a dedicated config directory relative to the application.
```python
@hydra.main(config_path="conf")
# or:
hydra.initialize(config_path="conf")
```

### No config directory
For applications that do not define config files next to the Python script (typically applications using only Structured Configs), it is recommended that
you pass `None` as the config_path, indicating that no directory should be added to the config search path.
This will become the default with [version_base](../version_base.md) >= "1.2"
```python
@hydra.main(config_path=None)
# or:
hydra.initialize(config_path=None)
```

### Using the application directory
Use the directory/module of the Python script.
This was the default behavior up to Hydra 1.0.  
This is not recommended as it can cause the surprising behavior outlined above.

```python
@hydra.main(config_path=".")
# or:
hydra.initialize(config_path=".")
```
