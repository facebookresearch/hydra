## Release tool

This tool keeps Hydra release operations package-aware. It knows about
`hydra-core`, the bundled plugins, and `hydra-configen`, and can check versions,
set versions, and build distributions.

Publishing is intentionally handled by GitHub Actions Trusted Publishing, not by
this local tool. The publish workflows call this tool to build artifacts, then
upload them from GitHub Actions.

### Package sets

- `set=hydra-core`: `hydra-core` only.
- `set=hydra-plugins`: all bundled Hydra plugins.
- `set=hydra-full-release`: `hydra-core` plus all bundled Hydra plugins.
- `set=configen`: `hydra-configen` only.
- `set=all`: `hydra-core`, `hydra-configen`, and all bundled Hydra plugins.

### Check published versions

```shell
python tools/release/release.py \
  action=check \
  set=hydra-full-release \
  repository=pypi
```

This reports whether each local version already exists on the selected
repository, with the latest non-yanked wheel shown as context.

### Set an explicit version

```shell
python tools/release/release.py \
  action=set_version \
  set=hydra-full-release \
  version=1.4.0.dev2
```

Use this for coordinated dev releases where `hydra-core` and the bundled plugins
should share the same version.

### Validate prepared versions

```shell
python tools/release/release.py \
  action=validate_versions \
  set=hydra-full-release \
  version=1.4.0
```

This fails if any selected package is not already at the expected version. The
publish workflow uses this to verify prepared release state before building and
uploading artifacts.

### Bump published packages

```shell
python tools/release/release.py action=bump set=hydra-full-release
```

This increments only packages whose local version exactly matches the latest
published version on PyPI. It is useful for continuing an existing release
series, but less useful when aligning multiple packages to a specific version.

### Build artifacts

Build only packages whose local version has not already been published to PyPI:

```shell
python tools/release/release.py \
  action=build \
  set=hydra-full-release \
  repository=pypi \
  clean_build_dir=true \
  require_artifacts=true \
  build_dir="${PWD}/dist"
```

Build every package in a set, ignoring repository state:

```shell
python tools/release/release.py \
  action=build \
  set=hydra-full-release \
  build_policy=all \
  clean_build_dir=true \
  build_dir="${PWD}/dist"
```

The GitHub publish workflows use the repository-aware form so already-published
files are not uploaded again.

The workflows also write a release summary listing the target repository,
publish mode, trigger, ref, commit, and every artifact that was built.

### Dev release

Run a dry run for a coordinated dev release:

```shell
python tools/release/release.py \
  action=dev_release \
  set=hydra-full-release \
  version=1.4.0.dev3
```

The dry run prints the selected packages, current local versions, target
versions, PyPI status for the target version, and the exact publish workflow
dispatch that would run. It also builds artifacts in a temporary release
workspace, runs `twine check`, and smoke-installs the built wheels without
dependencies. It does not commit, push, dispatch GitHub Actions, create or edit
a GitHub Release, or upload anything to PyPI.

To publish the dev release:

```shell
python tools/release/release.py \
  action=dev_release \
  set=hydra-full-release \
  version=1.4.0.dev3 \
  publish=true
```

Publishing requires a clean working tree whose current commit matches
`remote/<workflow_ref>`. The command applies the version bump, commits and
pushes it when the bump changes files, and dispatches `Publish to PyPI` with the
selected package set and expected version. It uses `workflow_ref=main` by
default; use `workflow_ref=<branch-or-tag>` for unusual cases such as publishing
a dev release from an already-published release line.

### Prepare and publish workflow responsibilities

Hydra release automation is split into prepare and publish phases.

Prepare release should:

- accept a release line, selected package set, and target version changes;
- derive the release kind from the selected target versions;
- derive the target branch from the release line and release kind;
- validate package versions against the release line and selected package set;
- compare selected packages against PyPI;
- produce a release-validation matrix;
- run release-only checks such as the core suite with all selected compatible
  plugins installed;
- create or update release-prep PRs when needed.

For release candidates, stable releases, and patch releases, generated
release-prep PRs are the maintainer approval surface for publishing. The PR body
must state clearly what happens when the PR is merged. Once release-prep PR
automation exists, merging such a PR should trigger PyPI publishing, and the PR
body must list the exact package set and version that will be published.

Publish should:

- revalidate the prepared release state;
- build selected package artifacts;
- check built artifacts;
- publish only selected package artifacts through GitHub Actions Trusted
  Publishing;
- eventually create or update the GitHub Release as a record of the published
  release.

The local release tool owns package metadata, version checks, repository
comparison, and artifact building. GitHub Actions owns release validation and
Trusted Publishing. GitHub Release state transitions are intended release
automation work, but are not wired into the current publish workflow.

The current `Prepare Release` workflow implements the validation part of this
split: it derives release kind and target branch, applies the target version
inside the disposable workflow checkout, checks selected packages against PyPI,
builds artifacts, and runs release validation. The current `Publish to PyPI`
workflow is manual-only. GitHub Release creation or edits do not trigger
publishing. Release-prep PR automation is planned but not implemented yet.
