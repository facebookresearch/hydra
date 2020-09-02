---
id: style_guide
title: Style Guide
sidebar_label: Style Guide
---

The code need to pass verification by the following tools:
 - `black .` : Automatic code formatting for Python
 - `flake8` : PEP8 compliance checker for Python, this includes copyright header verification
 - `isort .` : Ensure imports are sorted properly
 - `mypy --strict .` : Ensures code passes strict type checking
 - `yamllint .` : Ensures that yaml files are syntactically correct and properly indented.

The easiest way to run the required verifications is: 
 - `nox -s lint` : for the Hydra core
 - `nox -s lint_plugins` : for the included plugins

isort is a bit tricky to run for plugins. the best way to get it to sort the plugins imports is with the FIX environment
variable:
```
$ FIX=1 nox -s lint_plugins
```

It is also recommended that you install pre-commit hooks (use `pre-commit install`).
pre-commit will execute some of the above tests when you commit your code locally. 
You can disable it by appending `-n` to your commit command: `git commit -m wip -n`

Pull requests that do not lint will fail the automated testing.