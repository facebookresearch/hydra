---
id: release
title: Release process
sidebar_label: Release process
---

The release process may be automated in the future.

The versioning strategy is that the repo is configured to be on the next version and the version should be bumped AFTER the release, not before.

One should check that the version is the correct one against pypi before releasing.

### Hydra Release Process

- Checkout the release branch.
- Check the version in `hydra/__init__.py`. This should be one version higher than the version available on PyPI. If it is the same version as PyPI, bump the version locally.
- Create draft release notes using `towncrier build --draft`.
- If the draft notes are correct, update NEWS.md using `towncrier build`.
- Push the news file to release branch.
- Create a pip package: `python setup.py sdist bdist_wheel`
- Upload pip package: `python -m twine upload dist/*`
- Bump the version in `hydra/__init__.py`.
- Create a pull request to the release branch.
- Merge once the CI completes successfully.

### Plugin Release Process

- Checkout the release branch and switch directory to `plugins/name-of-plugin`.
- Check the version in `setup.py`. This should be one version higher than the version available on PyPI. If it is the same version as PyPI, bump the version locally.
- Create draft release notes using `towncrier build --draft  --version x.y`
- If the draft notes are correct, update NEWS.md using `towncrier build  --version x.y`
- Push the news file to release branch.
- Create a pip package: `python setup.py sdist bdist_wheel`
- Upload pip package: `python -m twine upload dist/*`
- Bump the version in `setup.py`.
- Create a pull request to the release branch.
- Merge once the CI completes successfully.
