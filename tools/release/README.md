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
- create or update release-prep PRs and draft GitHub Releases when needed.

Publish should:

- revalidate the prepared release state;
- build selected package artifacts;
- check built artifacts;
- publish only selected package artifacts through GitHub Actions Trusted
  Publishing;
- promote prepared draft GitHub Releases after successful publishing when a
  release tag is supplied.

The local release tool owns package metadata, version checks, repository
comparison, and artifact building. GitHub Actions owns release validation,
Trusted Publishing, and GitHub Release state transitions.

The current `Prepare Release` workflow implements the validation part of this
split: it derives release kind and target branch, applies the target version
inside the disposable workflow checkout, checks selected packages against PyPI,
builds artifacts, and runs release validation. Release-prep PR and draft GitHub
Release automation are planned but not implemented yet.
