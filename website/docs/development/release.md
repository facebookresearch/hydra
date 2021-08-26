---
id: release
title: Release process
sidebar_label: Release process
---

The release process may be automated in the future.

- Checkout main
- Update the Hydra version in `hydra/__init__.py`
- Update NEWS.md with towncrier
- Create a wheel and source dist for hydra-core: `python -m build`
- Upload pip package: `python -m twine upload dist/*`
 
