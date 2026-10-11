---
id: release
title: Release process
sidebar_label: Release process
---

Hydra publishes Python packages through GitHub Actions Trusted Publishing.
Maintainers use the local release tool and GitHub Actions to prepare,
validate, and publish releases. GitHub Actions performs the actual upload.

Do not run `twine upload` locally for Hydra releases.

## Release lines

Hydra releases are organized by release line:

- `main` prepares the active unreleased line.
- `x.y_branch` carries release candidates, stable releases, patch releases, and
  dev releases for an already-published `x.y` line.
- Tags and GitHub Releases use package versions such as `v1.4.0.dev1`,
  `v1.4.0rc1`, `v1.4.0`, or `v1.4.1`.
- Stable docs are versioned by line, such as `version-1.3`.

Release automation derives the target branch from the release line and target
versions:

- dev releases for the active unreleased line normally prepare from `main`;
- dev releases for an already-published release line prepare from that line's
  release branch;
- release candidates, stable releases, and patch releases prepare from the
  release branch, such as `1.4_branch`.

Use a branch override only for unusual recovery or workflow-testing cases. The
override is intentionally limited to `main` or the release line's
`x.y_branch`.

## Package sets

The release tool is package-set aware:

- `set=hydra-core`: `hydra-core` only.
- `set=hydra-plugins`: bundled Hydra plugins only.
- `set=hydra-full-release`: `hydra-core` plus bundled Hydra plugins.
- `set=configen`: `hydra-configen` only.
- `set=all`: `hydra-core`, bundled Hydra plugins, and `hydra-configen`.

The default Hydra release set is `hydra-full-release`. `hydra-configen` remains
a supported target, but it is not included in the default Hydra package release.

Use `only=<package_config_name>[,<package_config_name>...]` to narrow a package
set without adding a new named package set. Package config names are the keys in
`tools/release/conf/packages/`. For example, to target only the Optuna plugin
from the bundled plugin set:

```shell
python tools/release/release.py \
  action=check \
  set=hydra-plugins \
  only=hydra_optuna_sweeper \
  repository=pypi
```

Quote comma-separated filters so the quotes reach Hydra when passing more than
one package through a shell, for example
`only=\"hydra_optuna_sweeper,hydra_ray_launcher\"`.

## Versioning

The Hydra core version is defined in `hydra/__init__.py`. Plugin versions are
defined in each plugin package's `hydra_plugins/<plugin>/__init__.py`.

Bundled plugins support only the matching Hydra Core release line, including
its dev releases. For 1.4 plugins, require
`hydra-core>=1.4.0.dev1,<1.5.0.dev0`; update both bounds for later lines.
There are currently no bundled cross-line exceptions. Before release, run
`pytest tests/test_plugin_core_requirements.py` to check the generated package
metadata for both bounds.

For coordinated Hydra releases, set the core and bundled plugin versions
together:

```shell
python tools/release/release.py \
  action=set_version \
  set=hydra-full-release \
  version=1.4.0.dev2
```

Use PEP 440 version spelling, such as `1.4.0.dev2`, `1.4.0rc1`, or `1.4.0`.

Advance development versions immediately after publishing, not while preparing
the next release. The checked-in version should identify the next unpublished
release throughout development. For example, after publishing `1.4.0.dev2`, set
the coordinated package versions to `1.4.0.dev3`, commit, and push that bump
before resuming development.

The release kind is derived from the target version strings:

- `.devN` versions are dev releases;
- `rcN` versions are release candidates;
- final `x.y.0` versions are stable releases for a line;
- final `x.y.z` versions with `z > 0` are patch releases.

## Prepare release

Prepare release is the maintainer-controlled validation phase before publishing.
It should validate the release line, derive release kind from target versions,
derive the target branch, validate package versions against the selected package
set, compare selected packages against PyPI, and run release-grade checks.

Release-grade checks include the normal CI surface plus release-only checks such
as running the core test suite with all selected compatible plugins installed.
This keeps expensive low-yield checks out of normal PR CI while preserving them
for release decisions.

Use the `Prepare Release` workflow to run the current prepare checks. It accepts
the release line, target version, package set, and optional recovery-only branch
override. It derives the release kind and target branch, resolves the exact
commit that every job checks out, compares selected packages against PyPI for
the requested target version, verifies build artifacts for that version, and
runs the release validation matrix.

Prepare release must not upload artifacts to PyPI. The current workflow is a
validation step. It applies target versions only inside the disposable workflow
checkout. Creating release-prep PRs is part of the intended prepare phase but is
not automated yet.

For release candidates, stable releases, and patch releases, the generated
release-prep PR is the maintainer approval surface for publishing. The PR body
must say clearly what happens when the PR is merged. Once release-prep PR
automation exists, merging such a PR should trigger publishing to PyPI, and the
PR body must list the package set and exact version that will be published. Dev
releases may use a lighter manual publish flow and do not require a prepare PR.

## Local checks and artifact builds

Before publishing, compare the selected packages against the target repository:

```shell
python tools/release/release.py \
  action=check \
  set=hydra-full-release \
  repository=pypi
```

To build only artifacts whose exact local version is not already published to
the selected repository:

```shell
python tools/release/release.py \
  action=build \
  set=hydra-full-release \
  repository=pypi \
  clean_build_dir=true \
  require_artifacts=true \
  build_dir="${PWD}/dist"
twine check "${PWD}/dist"/*
```

Use `build_policy=all` only for local smoke tests where you intentionally want
to ignore repository state.

To verify that the selected package set is already prepared at the intended
version:

```shell
python tools/release/release.py \
  action=validate_versions \
  set=hydra-full-release \
  version=1.4.0
```

## PyPI

Use the PyPI workflow for real dev, release-candidate, and stable releases.

Every run pins one commit for every job. By default, the release tool pins its
final current commit, including a version-bump commit it creates as part of a
recovery, so later pushes cannot change what the workflow builds. Set
`commit=<full-commit-sha>` to release an existing commit after the branch has
already moved past it. The workflow also exposes the same commit input for
manual dispatches.

For dev releases, use the release tool's dev-release action. By default this is
a dry run: it shows the selected packages and versions, checks PyPI for the
target version, builds artifacts in a temporary release workspace, runs
`twine check`, smoke-installs the wheels without dependencies, and prints the
exact publish workflow dispatch that would run:

```shell
python tools/release/release.py \
  action=dev_release \
  set=hydra-full-release \
  version=1.4.0.dev3
```

To dry-run a single plugin dev release, narrow the selected package set:

```shell
python tools/release/release.py \
  action=dev_release \
  set=hydra-plugins \
  only=hydra_optuna_sweeper \
  version=1.4.0.dev3
```

To publish the dev release, rerun with `publish=true`. This first confirms that
the selected commit exists on the configured GitHub remote, without requiring
it to be the branch tip, and requires a clean working tree. It dispatches
`Publish to PyPI` with the selected package set, expected version, and the exact
commit being published. In the normal release flow, the selected packages are
already at this version because they were bumped immediately after the previous
release:

```shell
python tools/release/release.py \
  action=dev_release \
  set=hydra-full-release \
  version=1.4.0.dev3 \
  publish=true
```

The command can set, commit, and push the target version when the selected
packages do not already match it. Treat that as a recovery path, not the normal
release cadence.

If the branch was advanced to the next development version before the previous
one was published, dry-run the existing release commit directly:

```shell
python tools/release/release.py \
  action=dev_release \
  set=hydra-full-release \
  version=1.4.0.dev3 \
  commit=<full-commit-sha>
```

This archives the exact commit, requires every selected package to already have
the target version, and builds from that tree without changing the current
checkout. The commit must exist locally and on GitHub. After the dry run passes,
repeat the same command with `publish=true`. Explicit commit mode never sets
versions, creates a commit, or pushes the current branch.

Wait for the publish workflow run to finish before advancing anything. The run
builds and verifies artifacts, then pauses for `pypi-publish` environment
approval immediately before upload. Approve within seven days, before the
transient artifacts expire. Every job uses the pinned commit, so later pushes
cannot change the artifacts awaiting approval. A successful upload deletes the
transient artifacts. Once the run succeeds, immediately advance the selected
packages to the next development version, commit, and push the change before
resuming development:

```shell
python tools/release/release.py \
  action=set_version \
  set=hydra-full-release \
  version=1.4.0.dev4
```

Do not leave the development branch reporting a version that has already been
published.

The dev-release action uses `workflow_ref=main` by default. Use
`workflow_ref=<branch-or-tag>` for unusual cases such as publishing a dev release
from an already-published release line.

For release candidates, stable releases, and patch releases:

- Run prepare release for the target release line and package set.
- Check out the prepared target branch.
- Set the intended version with `tools/release/release.py`.
- For stable releases, update `NEWS.md` with towncrier.
- Commit and push the release changes.
- For a dry run, run the `Publish to PyPI` workflow manually with
  `publish=false`, selecting the package set and optional expected version.
- Review the workflow release summary for the exact artifacts that would be
  uploaded.
- Dispatch `Publish to PyPI` manually after the prepared release state is
  merged. The intended next step is to replace this with generated release-prep
  PRs where merging the PR triggers publishing to PyPI for the package set and
  version named in the PR body.
- Mark dev and release-candidate GitHub releases as prereleases.
- Approve the `pypi-publish` environment if prompted.

The `Publish to PyPI` workflow validates the selected package versions when an
expected version is provided, builds artifacts whose local versions are newer
than PyPI, checks them, smoke-installs built wheels without dependencies, and
publishes them through Trusted Publishing.

The PyPI workflow is manual-only. Manual runs default to `publish=false`; set
`publish=true` only when intentionally publishing from that manual run. Direct
GitHub Release creation or edits are not treated as publish approval and do not
trigger publishing.

## Release summaries

### Release-candidate corrections

Corrections to regressions introduced in a release candidate belong in that
candidate's news collection, rather than the final release's `news/` collection.
For Hydra 1.4.0rc2, keep these fragments under `news/rc/1.4.0rc2/` and render
the candidate notes with:

```shell
towncrier build --dir . --draft --version 1.4.0rc2 \
  --config news/rc/1.4.0rc2/towncrier.toml
```

Include that output in the rc2 release notes. The normal Towncrier configuration
ignores `news/rc/`, so these corrections are excluded from the final 1.4.0 notes.

### Publish workflow summary

The publish workflow writes a release summary to the GitHub Actions run. The
summary includes:

- target repository,
- publish mode,
- package set,
- expected version, when provided,
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
