---
id: slash_in_default
title: Slash in default option normalization
---

Hydra 1.4 normalizes Defaults List items that contain a slash in their value (e.g. `foo: bar/baz`) into their canonical format early during defaults composition.

### Changes to Defaults List Composition

Historically, you could specify a Defaults List entry like:

```yaml
# config.yaml
defaults:
  - foo: bar/baz
```

In Hydra 1.3, this resulted in:
* Config Group: `foo`
* Option: `bar/baz`

This caused surprising relative-defaults composition bugs inside `foo/bar/baz.yaml`. For example, any relative defaults declared within `foo/bar/baz.yaml` resolved relative to `foo` rather than the correct path `foo/bar`.

In Hydra 1.4, this shorthand is normalized early to:

```yaml
# config.yaml
defaults:
  - foo/bar: baz
```

This ensures that:
1. Config Group is `foo/bar`.
2. Option is `baz`.
3. Nested relative defaults in `foo/bar/baz.yaml` now resolve relative to `foo/bar` as expected.

### Breaking Surface & Package Changes

Normalizing `foo: bar/baz` to `foo/bar: baz` keeps the underlying config path but has the following package and override consequences:

1. **Override Key Change**: The override key changes from `foo` to `foo/bar`. If your command line overrides previously used `foo=bar/baz`, they must now use `foo/bar=baz`.
2. **Package Name Change**: By default, the package location of the option changes from `foo` to `foo.bar`. This can move where the composed dictionary keys are nested in the final output configuration.

### Migration

If your application relied on the old behavior where defaults nested inside `foo/bar/baz.yaml` resolved relative to `foo` (and thus you placed those nested configs at `foo/` instead of `foo/bar/`), Hydra 1.4 detects this mismatch and raises a clear error:

```
Could not load 'foo/bar/nested'.
However, a config was found at 'foo/nested', which indicates this application relies on the deprecated slash-containing default option shorthand behavior.
```

To fix this, either:
1. Move the nested config files to their correct directory location under the normalized group path (e.g. move `foo/nested.yaml` to `foo/bar/nested.yaml`), or
2. Explicitly rewrite the defaults list entries using canonical absolute paths.
