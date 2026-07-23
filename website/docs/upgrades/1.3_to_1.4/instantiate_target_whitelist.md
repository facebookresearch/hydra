---
id: instantiate_target_whitelist
title: Instantiate target whitelist
---

Running `hydra.utils.instantiate()` on config nodes from untrusted sources can
result in arbitrary code execution. This is a security risk because configs are
sometimes bundled with packages, models, checkpoints, or other downloaded
artifacts.

To address this, Hydra 1.4 deprecates resolving `_target_` values unless
trusted Python code at the callsite also provides `_target_whitelist_`.

For the full API reference, see
[Instantiating objects with Hydra](/docs/advanced/instantiate_objects/overview).

## Update direct calls

If your code calls `instantiate()` directly, pass the targets that call is
expected to resolve:

```python
from hydra.utils import instantiate

model = instantiate(cfg.model, _target_whitelist_="my_app.models.*")
```

## Update wrapped calls

If another function calls `instantiate()` internally, put the whitelist around
that call. This is also useful when calling `instantiate()` multiple times with
the same whitelist.

```python
from hydra.utils import target_whitelist

with target_whitelist("my_app.*"):
    framework_function(cfg)
```

## Framework authors

Framework authors should whitelist framework-owned targets around the internal
`instantiate()` calls that resolve framework config. Trust decisions for
application-owned targets should stay with the application. If framework code
also instantiates application objects, the application can wrap the framework
call with its own whitelist.

For example, a framework can whitelist its own launcher target:

```python
from hydra.utils import instantiate, target_whitelist

def train(cfg):
    with target_whitelist("my_framework.*"):
        launcher = instantiate(cfg.launcher)

    model = instantiate(cfg.model)
    launcher.run(model)
```

Application code can then add its own targets around the framework call:

```python
with target_whitelist("my_app.*"):
    train(cfg)
```

The inner framework whitelist adds `my_framework.*`; the outer application
whitelist adds `my_app.*`. The framework does not need to know which
application model targets are trusted.

## Plugin authors

Hydra 1.4 instantiates launcher and sweeper plugin configs non-recursively.
Hydra core instantiates only the registered plugin class. If your plugin config
contains nested `_target_` values, accept the nested config in the plugin
constructor and call `instantiate()` from plugin code with a plugin-owned
whitelist.

## Choose target patterns

Whitelist entries may be exact targets or package prefixes ending in `.*`.
The wildcard `*` by itself is not allowed.

Be careful with namespace packages and plugin namespaces. A whitelist entry such
as `my_app.*` allows any importable target under that Python namespace, including
modules contributed by other installed distributions. For shared namespaces,
prefer exact target names or narrower prefixes.

## Legacy behavior

To preserve legacy all-target behavior, use `UNSAFE_ALLOW_ALL_TARGETS`
explicitly:

```python
from hydra.utils import UNSAFE_ALLOW_ALL_TARGETS, instantiate

obj = instantiate(cfg.component, _target_whitelist_=UNSAFE_ALLOW_ALL_TARGETS)
```

Use this only when you intentionally want the old behavior.

Calling `instantiate()` without `_target_whitelist_` still works in Hydra 1.4,
but it emits a deprecation warning when resolving `_target_`.
Legacy mode continues to use Hydra's target blocklist as defense-in-depth.
