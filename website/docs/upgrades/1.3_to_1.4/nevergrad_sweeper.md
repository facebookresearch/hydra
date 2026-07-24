---
id: nevergrad_sweeper
title: Nevergrad Sweeper search-space configuration
---

Hydra 1.4 standardizes the Nevergrad Sweeper search-space configuration under
`hydra.sweeper.params`. The previous `hydra.sweeper.parametrization` field is
deprecated in Hydra 1.4 and will be removed in Hydra 1.5.

Move each search-space entry to `params` and express it using Hydra's override
grammar:

```yaml
hydra:
  sweeper:
    params:
      db: choice(mnist, cifar)
      lr: {init: 0.02, step: 2.0, log: true}
      dropout: interval(0, 1)
      batch_size: int(interval(4, 16))
```

The old configuration continues to work in Hydra 1.4 and emits a deprecation
warning. Configuring both fields at the same time is an error.

See the [Nevergrad Sweeper documentation](/plugins/nevergrad_sweeper.md) for
the complete search-space syntax.
