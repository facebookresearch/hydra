---
id: release
title: Release process
sidebar_label: Release process
---

The release process may be automated in the future.

- Checkout the release branch.
- Update the version in `hydra/__init__.py`.
- Create draft release notes using `towncrier build --draft`.
- If the draft notes are correct, update NEWS.md using `towncrier build`.
- Create a pip package: `python setup.py sdist bdist_wheel`
- Upload pip package: `python -m twine upload dist/*`


- Checkout the release branch and switch directory to `plugins/name-of-plugin`.
- Update the version in `setup.py`
- Create draft release notes using `towncrier build --draft  --version x.y`
- If the draft notes are correct, update NEWS.md using `towncrier build  --version x.y`
- Create a pip package: `python setup.py sdist bdist_wheel`
- Upload pip package: `python -m twine upload dist/*`
