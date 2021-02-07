---
id: release
title: Release process
sidebar_label: Release process
---

The release process may be automated in the future.

- Checkout master
- If releasing Hydra, update the version in `hydra/__init__.py`. For plugins, switch directory to `plugins/name-of-plugin` and update `setup.py`
- Create draft release notes using `towncrier build --draft`. In case of plugins, add an extra flag for version i.e., `towncrier build --draft  --version x.y`
- If the draft notes are correct, update NEWS.md using `towncrier build`. For plugins, use `towncrier build  --version x.y`
- Create a pip package: `python setup.py sdist bdist_wheel`
- Upload pip package: `python -m twine upload dist/*`
