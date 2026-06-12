---
id: overview
title: Developer Guide Overview
---

This guide assumes you have checked-out the [repository](https://github.com/facebookresearch/hydra).
It is recommended that you install Hydra in a project-local virtual environment
at `.venv`.

## Environment setup
Create and activate a virtual environment in the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
```

:::info NOTE
The core Hydra framework supports Python 3.10 through 3.14. You may need to create additional environments for different Python versions if CI detects issues on a supported version of Python.
:::

From the source tree, install Hydra in development mode with the following commands:

```bash
# install development dependencies
pip install -r requirements/dev.txt
# install Hydra in development (editable) mode
pip install -e .
```
