---
id: hydra_job_override_dirname
title: hydra.job.override_dirname
---

Hydra 1.4 deprecates `hydra.job.override_dirname` in favor of the `hydra_override_dirname` resolver.
The resolver keeps the same default behavior while making override dirname generation lazy and configurable at the use site.
Users can also replace it with their own resolver or interpolation when they need fundamentally different behavior.

```yaml title="Hydra 1.3"
hydra:
  sweep:
    subdir: ${hydra.job.override_dirname}
```

```yaml title="Hydra 1.4"
hydra:
  sweep:
    subdir: ${hydra_override_dirname:}
```

`hydra.job.config.override_dirname` is still used as the default configuration for `${hydra_override_dirname:}`:

```yaml
hydra:
  sweep:
    subdir: ${hydra_override_dirname:}/seed=${seed}
  job:
    config:
      override_dirname:
        exclude_keys:
          - seed
```

You can also pass options directly:

```yaml
hydra:
  sweep:
    subdir: '${hydra_override_dirname:{kv_sep: "-", item_sep: "_", exclude_keys: [seed]}}'
```

For more control, `element_resolver` can apply a custom OmegaConf resolver to each directory name element before the elements are joined.
The resolver must be registered separately before Hydra starts.
For example, this replaces path separators, including Windows path separators, with `_`:

```python
from omegaconf import OmegaConf

OmegaConf.register_resolver(
    "pathsafe",
    lambda value: str(value).replace("/", "_").replace("\\", "_"),
)
```

```yaml
hydra:
  sweep:
    subdir: '${hydra_override_dirname:{item_sep: "/", element_resolver: pathsafe}}'
```
