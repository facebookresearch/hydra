---
id: testing
title: Testing
sidebar_label: Testing
---

Hydra uses a test automation tool called [nox](https://github.com/theacodes/nox) to manage tests, linting, code coverage, etc.
`nox` will run all the configured sessions. You can see the full list of nox sessions with `nox -l` and run specific sessions
with `nox -s NAME` (you may need to quote the session name in some cases)

## With pytest
Run `pytest` at the repository root to run all the Hydra core tests.
To run the tests of individual plugins, use `pytest plugins/NAME`.

:::info NOTE
Some plugins support fewer versions of Python than the Hydra core.
:::

## With nox
See `nox -l`. a few examples:
* `nox -s test_core` will test Hydra core on all supported Python versions
* `nox -s "test_core-3.6(pip install)"` : Test on Python 3.6 with `pip install` as installation method
* `nox -s "test_plugins-3.8(pip install -e)"` : Test plugins on Python 3.8 with `pip install -e` as installation method
