1.1.5.rc1 (2021-05-18)
======================

### Features

- Enable support of Python 3.9 . ([#1203](https://github.com/facebookresearch/hydra/issues/1203))
- Support for deterministic functions in an Ax experiment via `is_noisy` input parameter ([#1395](https://github.com/facebookresearch/hydra/issues/1395))

### API Change (Renames, deprecations and removals)

- Switch Ax parser to use new Hydra command line syntax ([#870](https://github.com/facebookresearch/hydra/issues/870))
- Revert the use of "_" to separate the path element in keys for the Ax sweeper plugin. ([#913](https://github.com/facebookresearch/hydra/issues/913))

### Bug Fixes

- Correctly handle the Ax exception when the search space is exhausted. ([#1386](https://github.com/facebookresearch/hydra/issues/1386))
