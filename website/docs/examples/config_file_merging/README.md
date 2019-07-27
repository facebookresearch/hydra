---
id: example
title: Config file merging
sidebar_label: Config file merging
---
As your configuration becomes more complex, you may want to split it into multiple files.

Our config structure is getting a bit complex, so let's put everything into a config subdirectory:
```text
$ tree 4_config_file_merging/
4_config_file_merging/
├── conf
│   ├── config.yaml
│   ├── imagenet.yaml
│   └── nesterov.yaml
├── README.md
└── experiment.py
```

### experiment.py
Note the small change in config_path, all config files are relative to the location of the primary config.yaml:
```python
import hydra


@hydra.main(config_path='conf/config.yaml')
def experiment(cfg):
    print(cfg.pretty())


if __name__ == "__main__":
    experiment()
```
### imagenet.yaml:
```yaml
dataset:
  name: imagenet
  path: /datasets/imagenet
```
### nesterov.yaml:
```yaml
optimizer:
  type: nesterov
  lr: 0.001
```

However, you still want your code to operate on a single configuration object:
To support it, add a defaults block to the primary config file:

### config.yaml
```yaml
defaults:
  - imagenet
  - nesterov

# You can also add additional configuration in the primary config file.
# Those will be merged with the configs specified in the defaults section.
batch_size: 256
```
This functionality is similar to including files, but it's actually quite different:
The configs are merged into a single namespace. In this case they do not share any nodes so the
merge result looks like an include.

As before, we just tell Hydra what is the name of the main config:
### experiment.py
```python
import hydra


@hydra.main(config_path='config.yaml')
def experiment(cfg):
    print(cfg.pretty())


if __name__ == "__main__":
    experiment()

```

### Output
```yaml
$ python experiment.py
batch_size: 256
dataset:
  name: imagenet
  path: /datasets/imagenet
optimizer:
  lr: 0.001
  type: nesterov
```