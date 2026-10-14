# Instantiation isolation discussion notes

Discussion notes and reproduction for Hydra issue #3537. The experimental
`isolate` option is documented in the
[instantiation overview](../../website/docs/advanced/instantiate_objects/overview.md#instantiation-isolation).

```python
model = instantiate(cfg, isolate=True, _execution_whitelist_="my_app.*")
```

`isolate` is a keyword-only Python option. When omitted, the input config node's
`_isolate_` supplies the default for the entire invocation; if the config has no
such field, the mode is `False`. Explicit `isolate=True` or `isolate=False`
overrides the config default. `None` is not a valid mode. The implementation
uses an unspecified-value sentinel to distinguish omission from explicit `False`.

For example, a generated Structured Config can select isolation automatically:

```python
@dataclass
class ModelConf:
    _target_: str = "my_app.Model"
    _isolate_: bool = True
    sizes: list[int] = field(default_factory=lambda: [1, 2, 3])

model = instantiate(ModelConf, _execution_whitelist_="my_app.*")
shared = instantiate(ModelConf, isolate=False, _execution_whitelist_="my_app.*")
```

`_isolate_` is a reserved config directive and is not passed to constructors.
The selected invocation mode applies throughout traversal. Nested directives
cannot change it, even when they disagree with the root. A nested node's flag
becomes the default if that node is passed to a separate `instantiate()` call.
There is no scan for isolation directives elsewhere in the config tree.

A config field named `isolate` remains a normal target argument;
the call-site keyword is now consumed by Hydra, so it cannot also override a
target argument with that name.

## Behavior

- Copy the input configuration's ancestor tree, preserving the selected input
  and its interpolation context. Reuse the existing override-copy machinery.
- Apply current call-site override semantics, then eagerly resolve the entire
  selected input subtree before running constructors. Unrelated ancestor
  siblings are copied but are not independently resolved.
- Before every target call, copy direct OmegaConf positional and keyword
  arguments with private ancestor context, resolve them, and detach the
  copies. This also prepares arguments captured by `_partial_` factories.
- Apply the selected mode to targets traversed within the invocation. A separate
  `instantiate()` call made inside a constructor uses its own `isolate` option.
- Keep conversion modes, runtime-object override handling, exceptions, and
  execution checks from Hydra 1.4. Both modes retain #3545's strict call-site
  validation without coercion and require explicit object support for input
  configs. This is legacy isolation, not full Hydra 1.3 compatibility.

Copying and eager resolution deliberately restore the old costs. Config
argument identity and lazy dependencies on the source are lost. An earlier
constructor can no longer register a resolver needed by a later input value.
Eager resolution can also fail on values that lazy instantiation would never
access. Resolution runs on a private config; mutating a returned config does not
change the source config.

## Try it

Run from the repository root:

```sh
PYTHONPATH=. .venv/bin/python temp/repro/3537.py
.venv/bin/pytest -q tests/instantiate/test_isolation.py
```

The demo compares the exact local-dataclass failure, an ancestor interpolation,
and the pickle size of a three-item list with a large unrelated sibling. It
also demonstrates automatic selection from a generated config and explicit
call-site override in both directions.

## Boundaries and questions

- Isolation applies to direct OmegaConf target arguments, not arbitrary objects
  returned by a constructor. It does not guarantee pickleability. A detached
  Structured Config can still contain an unimportable class in its own schema
  metadata. Hydra partial factories still cannot be pickled.
- Direct non-container runtime call-site objects retain their current identity.
  Direct OmegaConf call-site arguments are copied and detached too. Copying a
  config can invoke `__deepcopy__` on objects stored in it, including already
  instantiated objects inside config arguments. This is not a sandbox for
  constructor or resolver side effects.
- Root containers returned from non-target configs are not automatically
  detached; isolation applies at target-call boundaries.
- Runtime overrides supplied when invoking an already-created partial factory
  do not go through this argument-preparation step.
- Copy optimizations are deferred; the existing input and per-argument copies
  remain in place.

The implementation uses a scoped context variable for argument preparation,
reset on success or failure, to avoid threading a new option through every
internal traversal helper. Input preparation continues to use the current
instantiation implementation rather than a second legacy implementation.

## Observed demo results

With Python 3.14 and OmegaConf 2.4.1rc1 in this checkout:

| Example | Default | `isolate=True` |
| --- | --- | --- |
| Local schema, model pickle | `PicklingError` | Succeeds, 654 bytes |
| Three-item list with large unrelated sibling | 6,439,710 bytes | 618 bytes |
| Ancestor interpolation after source width changes from 8 to 32 | `[32, 16]` | `[8, 16]` |

Both modes still pass `ListConfig` values in these examples. Byte counts depend
on the Python and OmegaConf versions.

## Validation

- 78 focused isolation tests pass, including config defaults and explicit
  precedence for dicts, OmegaConf configs, and dataclass classes/instances,
  runtime ancestor-container interpolation, null input handling, strict
  override validation, explicit input-object opt-in in both modes, and explicit
  read-only descendant and ancestor nodes during eager resolution.
- All 1,411 instantiation tests pass in the repo-local `.venv`.
- The complete `test_core-3.14` nox session passes: 3,990 core/build-helper
  tests, 25 skipped, and one expected failure, plus standalone-app and
  example-plugin checks.
- Complete core lint passes, including Ruff, Pyrefly, YAML lint, and Bandit.
- The website production build passes, including the migration-guide link.
- Copy strategy is unchanged; eager resolution now temporarily unlocks explicit
  read-only nodes in the private context tree.

The nox command was:

```sh
CC=cc CXX=c++ PYTHONPATH="$PWD:/tmp/hydra-oc241rc1" \
  NOX_PYTHON_VERSIONS=3.14 PIP_NO_INDEX=1 PIP_NO_BUILD_ISOLATION=0 \
  .venv/bin/nox -R -s test_core
```

Validation reused cached nox environments and the released OmegaConf 2.4.1rc1
source under `/tmp/hydra-oc241rc1`. The cached interpreter expects `clang`, which
is unavailable here; `CC` and `CXX` select the available compilers for fixture
subprocesses. Package builds ran with the cached dependencies and no build
isolation.

Review corrected two behavior defects: resolving a direct runtime OmegaConf
argument now leaves its original ancestor containers unchanged, including when
captured by a partial; a null `DictConfig` remains `None` without overrides and
still materializes when overrides supply fields. These preserve the experimental
isolation contract and current override semantics.
