1.2.2 (2026-10-21)
==================

### API Change (Renames, deprecations and removals)

- Breaking change: `ray_pkg_version` now expects installed distribution names,
  such as `PyYAML` instead of `yaml`. `hydra` remains an alias for `hydra-core`. ([#3566](https://github.com/hydra-ecosystem/hydra/issues/3566))

- Explicitly require Python 3.8 or newer, matching the `importlib.metadata`
  dependency already used in 1.2.1. ([#3566](https://github.com/hydra-ecosystem/hydra/issues/3566))

### Bug Fixes

- Security fix: read package versions from installed distribution metadata
  instead of importing modules. ([#3566](https://github.com/hydra-ecosystem/hydra/issues/3566))


1.2.1 (2024-02-15)
======================

- Upgrade to ray v2 ([#2713](https://github.com/facebookresearch/hydra/pull/2713))


1.2.0 (2022-05-17)
======================

### Features

- Add support for python 3.9 ([#1205](https://github.com/facebookresearch/hydra/issues/1205))
- Upgrade to ray 1.12.0 ([#2190](https://github.com/facebookresearch/hydra/issues/2190))


1.1.0 (2021-06-10)
=======================

### Configuration structure changes

- Add Ray SDK API configs - logging, create_update_cluster, teardown_cluster ([#1611](https://github.com/facebookresearch/hydra/issues/1611))

### Maintenance Changes

- Use autoscaler sdk instead of the CLI ([#1611](https://github.com/facebookresearch/hydra/issues/1611))


0.1.4 (2021-03-30)
==================

### Bug Fixes

- Fixed docker support in the RayLauncher plugin. ([#1191](https://github.com/facebookresearch/hydra/issues/1191))

### Maintenance Changes

- Pin Hydra 1.0 plugins to hydra-core==1.0.* to discourage usage with Hydra 1.1 ([#1501](https://github.com/facebookresearch/hydra/issues/1501))

