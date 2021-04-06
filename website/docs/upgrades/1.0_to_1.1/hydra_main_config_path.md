---
id: changes_to_hydra_main_config_path
title: Changes to @hydra.main()
---

Prior to Hydra 1.1, `@hydra.main()` default `config path` was the directory relative to the Python application (the script defining `@hydra.main()`)

This can cause surprising behavior, such as:
- Sibling directories are interpreted as config groups, which can lead to surprising results (See [#1533](https://github.com/facebookresearch/hydra/issues/1533)).
- The directory added automatically can have many files/directories - which will cause `--help` to be very slow as it's scanning for all config groups/config files (See [#759](https://github.com/facebookresearch/hydra/issues/759)).

To address these issues, Hydra 1.1 issues a warning if the config_path is not specified.
Your options are as follows:

### Dedicated config directory
Specify a directory like "conf" to use a dedicated config directory relative to the application.  
Recommended for applications with config files.
```python
@hydra.main(config_path="conf")
```

### No config directory
Do not add any directory to the config searchpath.
Recommended if you do not want to use configs files defined next to your Python script (Typically applications using only Structured Configs).
This will become the default in Hydra 1.2.
```python
@hydra.main(config_path=None)
```

### Using the application directory
Use the directory/module of the Python script.
This was the default behavior up Hydra 1.0.

```python
@hydra.main(config_path=".")
```
