---
id: style_guide
title: Style Guide
sidebar_label: Style Guide
---

The code needs to pass verification by the following tools:
 - `ruff format .` : Automatic code formatting for Python
 - `ruff check .` : Python linting, copyright verification, and import sorting
 - `pyrefly check` : Ensures code passes static type checking
 - `yamllint .` : Ensures that yaml files are syntactically correct and properly indented.

The easiest way to run the required verifications is:
 - `nox -s lint` : for everything
 - `nox -s lint-core` : for the Hydra core
 - `nox -s lint-plugins` : for the included plugins

Use the `FIX` environment variable to automatically format code and apply safe lint fixes:
```
$ FIX=1 nox -s lint-plugins
```

It is also recommended that you install pre-commit hooks (use `pre-commit install`).
pre-commit will execute some of the above tests when you commit your code locally. 
You can disable it by appending `-n` to your commit command: `git commit -m wip -n`

Pull requests that do not lint will fail the automated testing.
