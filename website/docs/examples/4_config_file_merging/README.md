---
id: example
title: Config file merging
sidebar_label: Config file merging
---
As your configuration becomes more complex, you may want to split it into multiple files:

#### imagenet.yaml:
```yaml
dataset:
  name: imagenet
  path: /datasets/imagenet
```
#### nesterov.yaml:
```yaml
optimizer:
  type: nesterov
  lr: 0.001
```

However, you still want your code to operate on a single configuration object:
To support it, add a defaults block to the primary config file:

#### config.yaml
```yaml
defaults:
  - imagenet
  - nesterov

# You can also add additional configuration in the primary config file.
# Those will be merged with the configs specified in the defaults section.
batch_size: 256
```
This functionality is similar to including files, but but it's actually quiet different:
The configs are merged into a single namespace. in this case they do not specify the same things so the
merge result looks like an include.

As before, we just tell Hydra what is the name of the main config:
#### config_file.py
```python
import hydra


@hydra.main(config_path='config.yaml')
def experiment(cfg):
    print(cfg.pretty())


if __name__ == "__main__":
    experiment()

```

#### Output
```yaml
$ python website/docs/examples/4_config_file_merging/config_file.py
batch_size: 256
dataset:
  name: imagenet
  path: /datasets/imagenet
optimizer:
  lr: 0.001
  type: nesterov
```