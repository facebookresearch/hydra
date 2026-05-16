---
id: release
title: Release process
sidebar_label: Release process
---

Hydra publishes Python packages through GitHub Actions Trusted Publishing.
Maintainers use the local release tool to set versions, compare local packages
against PyPI or TestPyPI, and build artifacts. GitHub Actions performs the
actual upload.

Do not run `twine upload` locally for Hydra releases.

## Package sets

The release tool is package-set aware:

- `set=hydra-core`: `hydra-core` only.
- `set=hydra-plugins`: bundled Hydra plugins only.
- `set=hydra-full-release`: `hydra-core` plus bundled Hydra plugins.
- `set=configen`: `hydra-configen` only.
- `set=all`: `hydra-core`, bundled Hydra plugins, and `hydra-configen`.

The default Hydra release set is `hydra-full-release`. `hydra-configen` remains
a supported target, but it is not included in the default Hydra package release.

## Versioning

The Hydra core version is defined in `hydra/__init__.py`. Plugin versions are
defined in each plugin package's `hydra_plugins/<plugin>/__init__.py`.

For coordinated Hydra releases, set the core and bundled plugin versions
together:

```shell
python tools/release/release.py \
  action=set_version \
  set=hydra-full-release \
  version=1.4.0.dev2
```

Use PEP 440 version spelling, such as `1.4.0.dev2`, `1.4.0rc1`, or `1.4.0`.

## Local checks

Before publishing, compare the selected packages against the target repository:

```shell
python tools/release/release.py \
  action=check \
  set=hydra-full-release \
  repository=pypi
```

Use `repository=testpypi` when preparing a TestPyPI upload.

To build only artifacts that are newer than the selected repository:

```shell
python tools/release/release.py \
  action=build \
  set=hydra-full-release \
  repository=pypi \
  clean_build_dir=true \
  require_artifacts=true \
  build_dir=dist
twine check dist/*
```

Use `build_policy=all` only for local smoke tests where you intentionally want
to ignore repository state.

## TestPyPI

Use TestPyPI to rehearse a release without touching real PyPI.

- Check out the branch or commit to test.
- Set the intended version with `tools/release/release.py`.
- Push the branch.
- Run the `Publish to Test PyPI` workflow manually.
- Select the branch containing the version bump.
- Use `publish=false` for a dry run. This builds and checks artifacts, then
  skips the upload job.
- Use `publish=true` to upload the checked artifacts to TestPyPI.
- Approve the `test-pypi-publish` environment if prompted.
- Review the workflow release summary for the exact artifacts that were, or
  would be, uploaded.
- After `publish=true`, install from TestPyPI in a clean environment and smoke
  test the packages.

## PyPI

Use the PyPI workflow for real dev, release-candidate, and stable releases.

- Check out `main`, or the release branch for a maintenance release.
- Set the intended version with `tools/release/release.py`.
- For stable releases, update `NEWS.md` with towncrier.
- Commit and push the release changes.
- For a dry run, run the `Publish to PyPI` workflow manually with
  `publish=false`.
- Review the workflow release summary for the exact artifacts that would be
  uploaded.
- To publish, create a GitHub release for the tag, for example `v1.4.0.dev2` or
  `v1.4.0`.
- Mark dev and release-candidate GitHub releases as prereleases.
- Approve the `pypi-publish` environment if prompted.

The `Publish to PyPI` workflow runs automatically when a GitHub release is
created. It builds artifacts whose local versions are newer than PyPI, checks
them, and publishes them through Trusted Publishing.

The PyPI workflow can also be triggered manually. Manual runs default to
`publish=false`; set `publish=true` only when intentionally publishing from that
manual run.

## Release summaries

Both publish workflows write a release summary to the GitHub Actions run. The
summary includes:

- target repository,
- publish mode,
- trigger,
- ref,
- commit,
- outcome,
- the full list of artifacts in `dist/`.

Use the summary as the maintainer-facing answer to "what would this publish?"

## Stable documentation

For a new stable release line, also update the website:

- Update the link to the latest stable release in `website/docs/intro.md`.
- If creating a new release branch, tag a new versioned copy of the docs using
  Docusaurus.
- Update `website/docusaurus.config.js` with a pointer to the new release
  branch on GitHub.
