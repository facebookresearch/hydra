---
id: instantiate_resolution
title: Instantiate resolution and call-site overrides
---

Hydra 1.4 changes when `hydra.utils.instantiate()` resolves configuration
values and how call-site arguments interact with the input configuration.

The examples on this page pass `_target_whitelist_` because trusted call-site
code is responsible for authorizing configured targets in Hydra 1.4. See the
[target whitelist migration guide](/docs/upgrades/1.3_to_1.4/instantiate_target_whitelist)
for the associated security and migration context.

## Benefits

`instantiate()` no longer deep-copies and eagerly resolves the full input
configuration before it starts instantiating targets. Instead, it traverses the
configuration and resolves each value when that value is needed.

This has several benefits:

- Unrelated parts of the configuration tree are not copied or resolved.
- A call-site argument can replace an unresolvable configured value without
  forcing Hydra to resolve the replaced value first.
- An earlier target can establish runtime state, such as registering a custom
  resolver, before a later argument is resolved.
- OmegaConf containers passed to a target are still copied, resolved while
  attached to their original parent, and then detached. This preserves the
  serialization safety of previous Hydra versions.

## Compatibility impact

Call-site arguments are now a separate runtime overlay. They determine the
arguments passed to the target, but they do not modify the input configuration
or affect how its interpolations resolve.

They are also no longer coerced or validated against the corresponding field
in an input Structured Config. Primitive values, native `list`, `tuple`, and
`dict` containers, and OmegaConf containers remain supported configuration
inputs. They retain Hydra's normal recursive merging, instantiation, and
conversion where applicable.

Hydra 1.4 intentionally changes the treatment of already-constructed dataclass
and attrs instances passed as call-site arguments. They are now regular runtime
objects and remain unchanged, even if they define `_target_`. Hydra no longer
implicitly converts them to Structured Configs, merges them with the input
configuration, or recursively instantiates them.

To use a dataclass or attrs instance as configuration, explicitly convert it
with `OmegaConf.structured(instance)`:

```python
from dataclasses import dataclass

from omegaconf import OmegaConf

from hydra.utils import instantiate


@dataclass
class ChildConfig:
    _target_: str = "builtins.dict"
    value: int = 10


child = ChildConfig()
cfg = {"_target_": "builtins.dict"}

runtime_result = instantiate(
    cfg,
    child=child,
    _target_whitelist_="builtins.dict",
)
assert runtime_result["child"] is child

config_result = instantiate(
    cfg,
    child=OmegaConf.structured(child),
    _target_whitelist_="builtins.dict",
)
assert config_result["child"] == {"value": 10}
```

For example:

```python
from omegaconf import OmegaConf

from hydra.utils import instantiate

cfg = OmegaConf.create(
    {
        "_target_": "builtins.dict",
        "b": 200,
        "c": "${b}",
    }
)

result = instantiate(cfg, b=99, _target_whitelist_="builtins.dict")
assert result == {"b": 99, "c": 200}
```

Hydra 1.3 merged `b=99` into a copied configuration before resolving `${b}`,
so `c` also became `99`. Hydra 1.4 leaves `cfg` unchanged, resolves `${b}`
against the original configuration, and independently passes the call-site
value `b=99` to the target.

If another argument should use the call-site value, pass that argument
explicitly as well:

```python
result = instantiate(
    cfg,
    b=99,
    c=99,
    _target_whitelist_="builtins.dict",
)
```
