---
id: release
title: Release process
sidebar_label: Release process
---

The release process is work in progress and will be automated in the future.

- Checkout master
- Update the Hydra version in `hydra/__init__.py`
- Update NEWS.rst with towncrier
- Create a pip package for hydra-core: `python setup.py sdist bdist_wheel`
- Upload pip package: python -m `twine upload dist/*`
 
