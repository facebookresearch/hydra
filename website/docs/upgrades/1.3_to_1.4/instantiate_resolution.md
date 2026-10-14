---
id: instantiate_resolution
title: Instantiate resolution and call-site overrides
---

Hydra 1.4 changes when `hydra.utils.instantiate()` resolves configuration
values and how call-site arguments interact with the input configuration.

Examples authorize targets with `_execution_whitelist_`; see the
[execution whitelist migration guide](/docs/upgrades/1.3_to_1.4/execution_whitelist).

## Benefits

`instantiate()` no longer eagerly resolves the full configuration before
constructing targets. Values resolve when needed during traversal or when a
target accesses a passed OmegaConf container. Calls on OmegaConf inputs without
overrides also avoid the former additional full-tree input copy.

- Unrelated values remain unresolved.
- Call-site arguments can replace unresolvable configured values.
- Earlier targets can establish runtime state, such as registering a resolver,
  before later values are accessed.

## Compatibility impact

Call-site overrides leave the input unchanged. Configured interpolations
resolve against those overrides in a private copy, preserving Hydra 1.3's result
without eager resolution:

```python
from omegaconf import OmegaConf

from hydra.utils import instantiate

cfg = OmegaConf.create({"_target_": "builtins.dict", "b": 200, "c": "${b}"})
result = instantiate(cfg, b=99, _execution_whitelist_="builtins.dict")
assert result == {"b": 99, "c": 99}
assert cfg.b == 200
```

Plain input containers and Structured Config defaults no longer automatically
accept arbitrary Python objects during default/raw input conversion. Without an
explicit `allow_objects` opt-in, such values, including object-valued `Any`
defaults, now raise `UnsupportedValueType`. Pass runtime objects as call-site
arguments instead:

```python
runtime = object()
cfg = {"_target_": "builtins.dict"}

# Previously accepted; now raises UnsupportedValueType:
# instantiate({**cfg, "payload": runtime}, _execution_whitelist_="builtins.dict")

result = instantiate(cfg, payload=runtime, _execution_whitelist_="builtins.dict")
assert result["payload"] is runtime
```

If an input config intentionally contains arbitrary objects, opt in when
constructing it:

```python
from dataclasses import dataclass

from omegaconf import OmegaConf


@dataclass
class Config:
    payload: object


config = Config(payload=object())
cfg = OmegaConf.structured(config, flags={"allow_objects": True})
```

Bare `OmegaConf.structured(instance)` is sufficient only when all values are
otherwise supported. Without the explicit opt-in, unsupported Structured Config
field annotations such as `object` are rejected during default/raw input
conversion. Use supported annotations, such as `Any` for an unrestricted
runtime argument, with a supported default such as `None`.

Call-site arguments are validated against declared configuration types without
coercion: `"1"` for an `int` field raises `ValidationError`, whereas Hydra 1.3
converted it to `1`. Unrestricted `Any` fields and additional parameters remain
runtime values. Validation does not replace supplied values or construct omitted
Structured Config defaults; factories run only when normal instantiation needs
them. Primitive and container arguments retain normal instantiation and
conversion semantics.

Plain Python overrides reject `???` and interpolation strings (`${...}`), even
inside native containers or constrained dataclass/attrs fields. Explicit
OmegaConf arguments may contain either; their interpolations remain unresolved
during validation. Future results follow
the argument container's own schema, which may be untyped, rather than acquiring
the destination field's schema. Configured interpolations retain normal
OmegaConf validation and conversion on access.

Dictionary overrides (`dict` or `DictConfig`) depend on the configured value:

- **Structured Config:** merge with schema validation, retaining unnamed fields
  and resolving configured interpolations against the merged values.
- **Otherwise, a mapping with `_target_`:** merge, retaining its target, settings
  and unnamed arguments. `_recursive_` controls instantiation, not merging.
- **Other mappings:** replace entirely, whereas Hydra 1.3 merged them.

Selection uses the configured value after interpolation. If it cannot be
resolved, the dictionary replaces it. For example:

```python
cfg = {
    "_target_": "builtins.dict",
    "tags": {"env": "prod", "team": "ml"},
    "optimizer": {"_target_": "builtins.dict", "lr": 0.1, "momentum": 0.5},
}

result = instantiate(
    cfg,
    tags={"env": "dev"},
    optimizer={"lr": 0.3},
    _execution_whitelist_="builtins.dict",
)
assert result["tags"] == {"env": "dev"}  # Hydra 1.3 retained team="ml"
assert result["optimizer"] == {"lr": 0.3, "momentum": 0.5}
```

To retain plain mapping keys, merge explicitly at the call-site with
`OmegaConf.merge(cfg["tags"], {"env": "dev"})`.

Dataclass and attrs instances passed at the call-site now retain their identity
as runtime objects, even if they define `_target_`. Hydra 1.3 treated them as
configurations; Hydra 1.4 does not implicitly convert, merge or recursively
instantiate them. Constrained fields still validate their type and field values
without reconstructing them. To use an instance as configuration, convert it
explicitly with `OmegaConf.structured(instance)`:

```python
from dataclasses import dataclass


@dataclass
class ChildConfig:
    _target_: str = "builtins.dict"
    value: int = 10


child = ChildConfig()
cfg = {"_target_": "builtins.dict"}

runtime_result = instantiate(
    cfg,
    child=child,
    _execution_whitelist_="builtins.dict",
)
assert runtime_result["child"] is child

config_result = instantiate(
    cfg,
    child=OmegaConf.structured(child),
    _execution_whitelist_="builtins.dict",
)
assert config_result["child"] == {"value": 10}
```

With `_recursive_=False`, `_convert_="none"`, and no call-site overrides,
the target receives the original `DictConfig`, `ListConfig`, or `TupleConfig`,
retaining its identity, lazy interpolations, ancestry, resolver cache and
inherited flags. The source tree is temporarily read-only throughout
instantiation, including constructors; Hydra restores its previous state
afterward. Constructors can explicitly mutate the source with OmegaConf's
`read_write()` context manager.

With overrides, configured containers come from the private resolution copy
without that temporary guard. Explicit OmegaConf arguments retain their identity
under the same recursion/conversion settings; other conversion modes behave as
documented.

To give targets independent OmegaConf arguments with fixed values, or avoid
serializing unrelated ancestors with a partial factory, use
[instantiation isolation](/docs/advanced/instantiate_objects/overview#instantiation-isolation):
pass `isolate=True`, or set `_isolate_: true` on the input config. An explicit
call-site value wins for the entire invocation, including nested targets. This
adds copying and eager-resolution costs and gives up source identity and lazy
dependencies. Hydra 1.4 override semantics still apply; pickleability is not
guaranteed.

For an independent argument, copy the container and pass the copy at the
call-site. Internal interpolations stay lazy; resolve before copying if they
depend on external ancestors:

```python
independent = OmegaConf.create(container)
# Alternative when interpolations depend on external ancestors:
independent = OmegaConf.create(OmegaConf.to_container(container, resolve=True))
```

## Partial factories and serialization

Hydra `_partial_` factories cannot be pickled. If work crosses a process
boundary, invoke the factory first and serialize the constructed object if its
type supports pickling, or recreate the factory in the receiving process.
Invoking a factory does not make the factory itself pickleable.
