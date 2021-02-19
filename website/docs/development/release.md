---
id: release
title: Release process
sidebar_label: Release process
---

The release process may be automated in the future.

The versioning strategy is that the repo is configured to be on the next version and the version should be bumped AFTER the release, not before.

One should check that the version is the correct one against pypi before releasing.

### Hydra Release Process

- Change branch to release branch and git pull to make sure on top of latest commit.
- Checkout a local branch for releasing.
- Check the version in `hydra/__init__.py`. This should be one version higher than the version available on [PyPI](https://pypi.org/project/hydra-core/). If it is the same version as PyPI, bump the version locally.
- Create draft release notes using `towncrier build --draft`.
- Make sure the draft notes look correct.
- Update NEWS.md using `towncrier build`.
- Create a pull request (to the release branch) with the NEWS.md updated, wait for review and CI to pass.
- Create a pip package: `python setup.py sdist bdist_wheel`
- Upload pip package: `python -m twine upload dist/*`
- [Create a release on GitHub](https://github.com/facebookresearch/hydra/releases/new)
    - Tag the version, tags start with v, for example v1.0.4
    - Tag target to be the release branch.
    - Set release title to be Hydra with release version, for example "Hydra 1.0.4"
    - Copy the release notes from added changes in NEWS.md from previous pull request.
    - Publish the release.
- Bump the version in `hydra/__init__.py`.
- Create a pull request to the release branch.
- Merge once the CI completes successfully.

### Plugin Release Process

- Change branch to release branch and git pull to make sure on top of latest commit.
- Checkout a local branch for releasing.
- Switch directory to `plugins/name-of-plugin`.
- Check the version in `setup.py`. This should be one version higher than the version available on PyPI. If it is the same version as PyPI, bump the version locally.
- Create draft release notes using `towncrier build --draft  --version x.y`
- Make sure the draft notes look correct.
- Update NEWS.md using `towncrier build  --version x.y`
- Create a pull request (to the release branch) with the NEWS.md updated, wait for review and CI to pass.
- Create a pip package: `python setup.py sdist bdist_wheel`
- Upload pip package: `python -m twine upload dist/*`
- Bump the version in `setup.py`.
- Create a pull request to the release branch.
- Merge once the CI completes successfully.
