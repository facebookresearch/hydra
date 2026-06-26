---
id: hydra_main
title: The @hydra.main() Decorator
sidebar_label: "@hydra.main() Decorator"
---

import {ExampleGithubLink} from "@site/src/components/GithubLink"

`@hydra.main()` is the primary entry point for any Hydra application. It wraps your
main function, initializes Hydra, composes the configuration from all configured
sources, and then calls your function with the resulting `DictConfig` object.

## Basic Usage

```python title="my_app.py"
from omegaconf import DictConfig, OmegaConf
import hydra

@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()
```

## Signature

```python
def main(
    config_path: Optional[str] = _UNSPECIFIED_,
    config_name: Optional[str] = None,
    version_base: Optional[str] = _UNSPECIFIED_,
) -> Callable[[TaskFunction], Any]:
    ...
```

## Parameters

### `config_path`

**Type:** `Optional[str]`
**Default:** Depends on `version_base` (see below)

The directory where Hydra will search for configuration files. This path is added
to [Hydra's Config Search Path](search_path.md).

- **Relative path** — resolved relative to the Python file containing the
  `@hydra.main()` decorator.
- **`pkg://` prefix** — treats the path as a Python package name and adds it to
  the search path using the package's location. For example:
  `config_path="pkg://mypackage.conf"`.
- **`None`** — no directory is added to the search path. Use this when all
  configs are provided through other means (e.g., a `SearchPathPlugin`, a
  `ConfigStore`, or `hydra.searchpath` overrides).

:::info Default value and `version_base`
The default value of `config_path` changes depending on `version_base`:

- `version_base="1.2"` or `version_base=None` (current version defaults): `config_path` defaults to `None`.
- `version_base="1.1"` or earlier: `config_path` defaults to `"."` (the directory of the calling script).

When `version_base` is not specified at all, Hydra 1.2 issues a deprecation warning
and falls back to the 1.1 behavior (`config_path="."`). It is strongly recommended
to always specify `version_base` explicitly.
:::

**Examples:**

```python
# Config files live in a "conf/" directory next to my_app.py
@hydra.main(version_base=None, config_path="conf", config_name="config")

# Config files are in a Python package
@hydra.main(version_base=None, config_path="pkg://mypackage.conf", config_name="config")

# No file-based config directory — all config comes from ConfigStore or plugins
@hydra.main(version_base=None, config_path=None, config_name="config")
```

---

### `config_name`

**Type:** `Optional[str]`
**Default:** `None`

The name of the **primary config file** to load (without the `.yaml` extension).
Hydra searches for `<config_name>.yaml` inside the directories on the
[Config Search Path](search_path.md).

When `config_name=None`, Hydra starts with an empty config. This is useful when
your application is fully configured using [Structured Configs](../tutorials/structured_config/intro.md)
registered in the `ConfigStore`, or when all configuration is supplied on the
command line.

**Examples:**

```python
# Loads conf/config.yaml as the primary config
@hydra.main(version_base=None, config_path="conf", config_name="config")

# No primary config file; config is built from ConfigStore / CLI overrides only
@hydra.main(version_base=None, config_path=None, config_name=None)
```

---

### `version_base`

**Type:** `Optional[str]`
**Default:** `_UNSPECIFIED_` (triggers a deprecation warning)

Controls Hydra's backwards-compatibility behavior. See the
[version_base documentation](../upgrades/version_base.md) for a complete
description of all behavioral changes gated behind each version.

| Value | Behavior |
|---|---|
| `_UNSPECIFIED_` (omitted) | Uses 1.1 defaults; **issues a deprecation warning** |
| `None` | Uses the current minor version's defaults (recommended for new projects) |
| `"1.1"` | Enables Hydra 1.1 defaults (e.g., `config_path="."`, `chdir=True`) |
| `"1.2"` | Enables Hydra 1.2 defaults (e.g., `config_path=None`, `chdir=False`) |

**Best practice:** always specify `version_base` explicitly to avoid surprises
when upgrading Hydra:

```python
# New project — opt into current defaults
@hydra.main(version_base=None, config_path="conf", config_name="config")

# Existing project that relies on 1.1 behavior
@hydra.main(version_base="1.1", config_path="conf", config_name="config")
```

---

## What `@hydra.main()` Does at Runtime

When you call `my_app()` (i.e., the decorated function) from `__main__`:

1. **Parses command-line arguments** using Hydra's argument parser (supports
   overrides, `--multirun`, `--config-dir`, `--info`, etc.).
2. **Initializes the global Hydra state**, including logging, the working directory,
   and the Config Search Path.
3. **Composes the final configuration** by merging the primary config, config
   groups, defaults list, and any command-line overrides.
4. **Sets `HydraConfig`** (see [below](#hydraconfig-global-state)) with the
   composed Hydra-internal configuration.
5. **Calls your task function** with the composed `DictConfig` as its only argument.

In `--multirun` mode, steps 3–5 are repeated once per combination of swept
parameter values.

---

## Return Value

`@hydra.main()` does not expose a return value from the task function to the
caller. If your task function raises an exception, that exception propagates
normally.

:::note
In `--multirun` mode the decorator may call your function multiple times.
Any return value from individual calls is discarded.
:::

---

## `HydraConfig` Global State

Before calling your task function, `@hydra.main()` sets the global
`HydraConfig` singleton with Hydra-internal configuration such as the current
job name, sweep overrides, working directory, and runtime info.

You can access this inside your task function:

```python
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig
import hydra

@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    hydra_cfg = HydraConfig.get()
    print("Job name:    ", hydra_cfg.job.name)
    print("Output dir:  ", hydra_cfg.runtime.output_dir)
    print("Overrides:   ", hydra_cfg.overrides.task)

if __name__ == "__main__":
    my_app()
```

`HydraConfig.get()` raises `ValueError` if called before `@hydra.main()` has
initialized Hydra (e.g., during import time or in unit tests that do not use the
decorator). Use `HydraConfig.initialized()` to check first if needed.

---

## Common Usage Patterns

### Minimal app (no config file)

```python title="my_app.py"
from omegaconf import DictConfig
import hydra

@hydra.main(version_base=None)
def my_app(cfg: DictConfig) -> None:
    print(cfg)

if __name__ == "__main__":
    my_app()
```

### App with a config file

```python title="my_app.py"
from omegaconf import DictConfig, OmegaConf
import hydra

@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()
```

```yaml title="conf/config.yaml"
db:
  host: localhost
  port: 3306
```

### App with Structured Config

```python title="my_app.py"
from dataclasses import dataclass
from omegaconf import DictConfig, OmegaConf
import hydra
from hydra.core.config_store import ConfigStore

@dataclass
class DBConfig:
    host: str = "localhost"
    port: int = 3306

cs = ConfigStore.instance()
cs.store(name="config", node=DBConfig)

@hydra.main(version_base=None, config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()
```

### Multirun sweep

```bash
# Sweeps over all combinations of db.host and db.port
python my_app.py --multirun db.host=localhost,remotehost db.port=3306,5432
```

---

## Decorating an Already-Decorated Function

`@hydra.main()` can wrap a function that already has another decorator, provided
the inner decorator uses `@functools.wraps`. See
[Decorating the main function](decorating_main.md) for details and requirements.

---

## Relation to the Compose API

`@hydra.main()` is the standard way to use Hydra in a script. If you need to
compose a config inside a unit test, a Jupyter notebook, or any code that
cannot rely on the command line, use the
[Compose API](compose_api.md) instead.
