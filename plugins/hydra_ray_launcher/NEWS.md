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

