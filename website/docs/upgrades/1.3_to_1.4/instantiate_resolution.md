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
- With `_recursive_=False` and the default `_convert_="none"`, Hydra no longer
  makes a final copy of OmegaConf containers before the target call. Containers
  passed through from the input tree retain their identity, lazy
  interpolations, ancestor context, resolver cache, and inherited flags.

## Compatibility impact

Call-site arguments are now a separate runtime overlay. They determine the
arguments passed to the target without modifying the input configuration. A
configured interpolation that survives the overlay still resolves against the
values being passed to the target, so an argument the call-site replaces is
seen by the interpolations that depend on it.

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

The input configuration is left unchanged, while the interpolation still sees
the value passed at the call-site:

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
assert result == {"b": 99, "c": 99}
assert cfg.b == 200
```

Hydra 1.3 achieved this by merging `b=99` into a copied configuration before
resolving `${b}`. Hydra 1.4 resolves the interpolation against the effective
configuration being instantiated instead, so `cfg` itself is never modified and
a configured value that the call-site replaces is not resolved at all.

With `_recursive_=False` and `_convert_="none"`, OmegaConf containers are also
no longer copied and detached before the target call. The target receives the
same `DictConfig`, `ListConfig`, or `TupleConfig` object from the input tree.
Mutations made by the target are therefore visible through the original
configuration, and an attached subtree retains its ancestor configuration when
stored or serialized. Other conversion modes retain their documented
conversion behavior.

To pass an independent Config object instead, create one explicitly:

```python
cfg = OmegaConf.create(
    {
        "_target_": "builtins.dict",
        "_recursive_": False,
        "payload": {"value": 10, "alias": "${.value}"},
    }
)
independent = OmegaConf.create(cfg.payload)
result = instantiate(
    cfg,
    payload=independent,
    _target_whitelist_="builtins.dict",
)
assert result["payload"] is independent
```

`OmegaConf.create()` preserves lazy interpolations within the copied container.
If an interpolation depends on an ancestor outside that container, resolve it
while copying:

```python
independent = OmegaConf.create(
    OmegaConf.to_container(cfg.payload, resolve=True)
)
```

A container passed through without recursion is resolved by the caller rather
than by Hydra, so it keeps its identity and its own ancestor context even when
another argument is overridden at the call-site. Its interpolations therefore
resolve against the input configuration.
