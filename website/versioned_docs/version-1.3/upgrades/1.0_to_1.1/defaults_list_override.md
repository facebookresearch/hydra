---
id: defaults_list_override
title: Defaults List Overrides
---
Hydra versions prior to 1.1 supported overriding of Hydra config groups via the Defaults List in this manner:
```yaml {3}
defaults:
 - model: resnet50
 - hydra/launcher: submitit
```
As of Hydra 1.1, Config group overrides must be marked explicitly with the `override` keyword:
```yaml {3}
defaults:
 - model: resnet50
 - override hydra/launcher: submitit
```

The Defaults List is described [here](/advanced/defaults_list.md).

:::warning
Omitting the `override` keyword when overriding Hydra's config groups will result in an error in Hydra 1.2
:::