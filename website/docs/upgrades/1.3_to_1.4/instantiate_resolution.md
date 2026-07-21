---
id: instantiate_resolution
title: Instantiate resolution and call-site overrides
---

Hydra 1.4 changes when `hydra.utils.instantiate()` resolves configuration
values and how call-site arguments interact with the input configuration.

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
in an input Structured Config. They remain runtime inputs, subject to Hydra's
normal recursive instantiation and conversion of the supplied value.

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
