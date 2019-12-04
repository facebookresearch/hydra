---
id: release
title: Release process
sidebar_label: Release process
---

The release process may be automated in the future.

- Checkout master
- Update the Hydra version in `hydra/__init__.py`
- Update NEWS.md with towncrier
- Create a pip package for hydra-core: `python setup.py sdist bdist_wheel`
- Upload pip package: `python -m twine upload dist/*`
 
