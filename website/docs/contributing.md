---
id: contributing
title: Contributing
sidebar_label: Contributing
---

## Getting started
Checkout this repository.
### Installing Hydra and plugins
It is recommended that you install Hydra in a virtual environment like conda or virtualenv.

Install Hydra and all the included plugins in development mode with the following commands:
```
pip install -e .[dev] && find ./plugins/ -name setup.py | xargs dirname | xargs pip install  -e
```

### Pre commit hooks
It is highly recommended that you install pre commit hooks.
Pre commit hooks are:
 - black : automatic code formatting for Python
 - flake8: pep8 compliance checker for Python
any PR that does not pass black and flake8 will fail the automated testing.

```
pre-commit install 
```

You can uninstall Hydra and all the included plugins with:
```
pip uninstall -y hydra && find ./plugins/ -name setup.py |\
xargs -i python {}  --name | xargs pip uninstall  -y
```

## Testing
TODO: document in more details.

For now, you can use nox:
`nox -l` will list all available sessions.
You can use `nox -s NAME` to run a specific session.


For example:
 * `nox -s test_core` will test Hydra core on all supported Python versions
 * `nox -s lint` will lint the code. 

