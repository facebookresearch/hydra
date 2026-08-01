---
id: prepare_for_1_4
title: Hydra 1.4 preparation guide
---

Hydra 1.4 removes several years of accumulated compatibility behavior. Use
this checklist to prepare an application while it is still running on Hydra
1.3.

If the application will remain on Hydra 1.3, pin the dependency to
`hydra-core>=1.3,<1.4` to prevent an unintended upgrade.

## Prepare for version_base removal

`version_base` does not provide distinct Hydra 1.2 and 1.3 compatibility
modes. It selects between the old 1.1 behavior and the behavior that has been
used since Hydra 1.2.

Hydra 1.3.5 emits `Hydra14MigrationWarning` when `version_base` is omitted or
set to `"1.1"`. Those are the two cases that select behavior removed by Hydra
1.4.

Before upgrading, set `version_base="1.3"` and run the application tests:

```python
@hydra.main(version_base="1.3", config_path="conf", config_name="config")
def app(cfg: DictConfig) -> None:
    ...
```

This temporary setting makes the surviving behavior explicit while the
application still runs on Hydra 1.3. `version_base=None`, `"1.2"`, and `"1.3"`
all select that behavior in Hydra 1.3, but applications using `"1.2"` must
change it to `"1.3"` because Hydra 1.4 no longer accepts the 1.2 compatibility
level.

After upgrading to Hydra 1.4, remove `version_base`. Hydra 1.4 rejects `"1.2"`
and older values, and warns on all other explicit values. Hydra 1.5 removes
the parameter completely.

### Hydra 1.1 compatibility and deprecated behavior removed

Hydra 1.4 removes the behavior selected by `version_base="1.1"` and other
behavior deprecated during the Hydra 1.1 migration:

- The default config search path changes from the calling directory to no
  added directory. Set `config_path` explicitly when the application has a
  config directory. See [Changes to @hydra.main() and hydra.initialize()](../1.1_to_1.2/hydra_main_config_path.md).
- `hydra.job.chdir` defaults to `False`. Set it explicitly if the application
  must run from Hydra's output directory. See [Changes to the job working directory](../1.1_to_1.2/changes_to_job_working_dir.md).
- Config files must use the `.yaml` extension rather than `.yml`.
- Replace old Defaults List entries such as `{group: option, optional: true}`
  with `optional group: option`.
- Defaults List entries that replace Hydra config groups need the `override`
  keyword. See [Defaults List overrides](../1.0_to_1.1/defaults_list_override.md).
- Replace indexed Defaults List interpolations such as
  `${defaults.0.dataset}`. See [Defaults List interpolation](../1.0_to_1.1/defaults_list_interpolation_changes.md).
- Remove a `# @package _group_` header to use the default package. Replace
  other uses of `_group_` or `_name_` with a literal package. See
  [Changes to package headers](../1.0_to_1.1/changes_to_package_header.md).
- Remove the `strict` argument from `hydra.compose()`. See the
  [strict mode migration guide](../0.11_to_1.0/strict_mode_flag_deprecated.md)
  for replacements for its individual behaviors.
- Replace automatic ConfigStore schema matching with explicit config extension
  through the Defaults List. See
  [Automatic schema matching](../1.0_to_1.1/automatic_schema_matching.md).

Explicit `config_path` and `hydra.job.chdir` settings take precedence over the
old compatibility defaults.

### Hydra 1.2 migration artifacts removed

Hydra 1.4 also removes migration paths retained after Hydra 1.2:

- Replace `TargetConf` with a Structured Config containing a `_target_` field.
- Import `compose()` and the initialization functions from `hydra` instead of
  `hydra.experimental`.
- Set `hydra.job.chdir` to `True` or `False`; `null` is no longer accepted.
- Callers of the internal `run_job()` API must pass `hydra_context`.
- Third-party Sweepers must use the `HydraContext` supplied to `setup()` to
  access the config loader.
- Optuna Sweeper users must replace `hydra.sweeper.search_space` with
  `hydra.sweeper.params`. See
  [Sweeper configuration changes](../1.1_to_1.2/changes_to_sweeper_config.md).

### Staying on Hydra 1.3

Applications intentionally pinned to Hydra 1.3 can suppress only this release
migration warning before Hydra initialization:

```python
import warnings

from hydra.errors import Hydra14MigrationWarning

warnings.filterwarnings("ignore", category=Hydra14MigrationWarning)
```

This does not suppress unrelated warnings or migration warnings for later
Hydra releases.

## Check runtime and dependency compatibility

- Hydra 1.4 supports Python 3.10 through 3.14. Move the application to a
  supported Python version before upgrading Hydra.
- Check that every Hydra launcher and sweeper used by the application has a
  Hydra 1.4-compatible release.
- Hydra 1.4 uses OmegaConf 2.4, which preserves tuples as immutable
  `TupleConfig` objects. Use `OmegaConf.is_sequence()` when code accepts both
  `ListConfig` and `TupleConfig`. If the value must be mutable, use a list
  input or a `list` annotation instead. See the
  [OmegaConf tuple migration guide](https://omegaconf.readthedocs.io/en/latest/tuple_migration.html).

## Review direct uses of instantiate

Applications that call `hydra.utils.instantiate()` should review both
dedicated migration guides:

- [Instantiate resolution and call-site overrides](/docs/upgrades/1.3_to_1.4/instantiate_resolution)
- [Instantiate target whitelist](/docs/upgrades/1.3_to_1.4/instantiate_target_whitelist)

In particular, call-site dataclass and attrs instances are passed through as
runtime objects, resolution is lazy, and Config objects used with
`_recursive_=False` are no longer copied before the target call. Target
resolution without a call-site whitelist is deprecated in Hydra 1.4.

## Check removed and restricted behavior

- Remove the unsupported Torchrun launcher and anything imported from Hydra's
  former `contrib` plugin area.
- Remove uses of the experimental `on_compose_config` callback.
- Remove parent traversal such as `../group/option` from Defaults List config
  paths.

## Address Hydra 1.4 deprecations

These changes still have compatibility paths in Hydra 1.4, but migrating early
reduces future work:

- Replace `hydra.job.override_dirname` with the
  [`hydra_override_dirname` resolver](/docs/upgrades/1.3_to_1.4/hydra_job_override_dirname).
- Nevergrad Sweeper users should move `hydra.sweeper.parametrization` to
  [`hydra.sweeper.params`](/docs/upgrades/1.3_to_1.4/nevergrad_sweeper).

## Validate the application

Before installing Hydra 1.4:

1. Run every application entry point on the latest Hydra 1.3 release with
   `version_base="1.3"`.
2. Address all Hydra and OmegaConf warnings.
3. Test config composition, single runs, multiruns, working directories, and
   the launcher and sweeper plugins used in production.
4. In a separate environment, test against the latest Hydra development
   release with `pip install --upgrade --pre hydra-core`. Do not add the
   unreleased version to production dependencies.

This guide will be updated as the remaining Hydra 1.4 work is completed.
