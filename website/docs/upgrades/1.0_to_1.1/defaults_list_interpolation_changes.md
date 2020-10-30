---
id: defaults_list_interpolation
title: Defaults List interpolation
hide_title: true
---

## Defaults List interpolation
The defaults lists are used to compose the final config object.
Hydra supports a limited form of interpolation in the defaults list.
The interpolation style described there is deprecated in favor of a cleaner style more
appropriate to recursive default lists.

## Migration examples

For example, the following snippet from Hydra 1.0 or older: 
```yaml
defaults:
  - dataset: imagenet
  - model: alexnet
  - dataset_model: ${defaults.0.dataset}_${defaults.1.model}
```

Changes to this in Hydra 1.1 or newer:
```yaml
defaults:
  - dataset: imagenet
  - model: alexnet
  - dataset_model: ${dataset}_${model}
```

The new style is more compact and does not require specifying the exact index of the element in the defaults list.
This is enables interpolating using config group values that are coming from recursive defaults.

Note that:
 - This is non-standard interpolation support that is unique to the defaults list
 - interpolation keys in the defaults list can not access values from the composed config because it does not yet 
 exist when Hydra is processing the defaults list

:::warning
Support for the old style will be removed in Hydra 1.2.