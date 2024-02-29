---
id: testing
title: Testing
sidebar_label: Testing
---

Hydra uses [nox](https://github.com/theacodes/nox) - a build automation tool - to manage tests, linting, code coverage, etc.
The command `nox` will run all the configured sessions. List the sessions using `nox -l` and 
run specific sessions with `nox -s NAME` (you may need to quote the session name in some cases)

## Testing with pytest
Run `pytest` at the repository root to run all the Hydra core tests.
To run the tests of individual plugins, use `pytest plugins/NAME` (The plugin must be installed).

:::info NOTE
Some plugins support fewer versions of Python than the Hydra core.
:::

## Testing with nox
See `nox -l`. a few examples:
* `nox -s test_core` will test Hydra core on all supported Python versions
* `nox -s "test_plugins-3.8"` will test plugins on Python 3.8.
* `nox -s "test_plugins-3.8"` will test plugins on Python 3.8.

The `noxfile.py` is checking some environment variables to decide what to run. For example,
to test a single plugin:
```shell {4}
$ PLUGINS=hydra_colorlog nox -s test_plugins-3.8
Operating system        :       Linux
NOX_PYTHON_VERSIONS     :       ['3.8', '3.9', '3.10', '3.11']
PLUGINS                 :       ['hydra_colorlog']
SKIP_CORE_TESTS         :       False
FIX                     :       False
VERBOSE                 :       0
INSTALL_EDITABLE_MODE   :       0
nox > Running session test_plugins-3.8
...
```
