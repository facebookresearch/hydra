---
id: config_path_changes
title: Config path changes
---

## Overview
Hydra 1.0 adds a new `config_name` parameter to `@hydra.main()` and changes the meaning of the `config_path`.
Previously, `config_path` encapsulated two things:
- Search path relative to the declaring python file.
- Optional config file (.yaml) to load.

Having both of those things in the same parameter does not work well if you consider configs that are not files 
such as Structured Configs. In addition, it prevents overriding just the `config_name` or just the `config_path`

A second change is that the `config_name` no longer requires a file extension. For configs files the `.yaml` extension
will be added automatically when the file is loaded.

This change is backward compatible, but support for the old style is deprecated and will be removed in the next major Hydra version.

## Migration examples

```python title="Hydra 0.11"
@hydra.main(config_path="config.yaml")
```
Becomes: 
```python title="Hydra 1.0"
@hydra.main(config_name="config")
```

And
```python title="Hydra 0.11"
@hydra.main(config_path="conf/config.yaml")
```

Becomes:
```python title="Hydra 1.0"
@hydra.main(config_path="conf", config_name="config")
```
