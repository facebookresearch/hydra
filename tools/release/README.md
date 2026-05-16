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

This compares local package versions with the latest non-yanked wheel on the
selected repository. Use `repository=testpypi` when preparing a TestPyPI upload.

### Set an explicit version

```shell
python tools/release/release.py \
  action=set_version \
  set=hydra-full-release \
  version=1.4.0.dev2
```

Use this for coordinated dev releases where `hydra-core` and the bundled plugins
should share the same version.

### Bump published packages

```shell
python tools/release/release.py action=bump set=hydra-full-release
```

This increments only packages whose local version exactly matches the latest
published version on PyPI. It is useful for continuing an existing release
series, but less useful when aligning multiple packages to a specific version.

### Build artifacts

Build only packages whose local version is newer than PyPI:

```shell
python tools/release/release.py \
  action=build \
  set=hydra-full-release \
  repository=pypi \
  clean_build_dir=true \
  require_artifacts=true \
  build_dir="${PWD}/dist"
```

Use `repository=testpypi` to compare against TestPyPI instead.

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
