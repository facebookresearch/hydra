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
- Update the link to the latest stable release in `website/docs/intro.md`
- If you are creating a new release branch:
  - [tag a new versioned copy of the docs using docusaurus](https://docusaurus.io/docs/versioning#tagging-a-new-version)
  - update `website/docusaurus.config.js` with a pointer to the new release branch on github
