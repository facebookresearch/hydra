---
id: config_splitting
title: Splitting a configuration file
sidebar_label: Splitting a configuration file
---
As your configuration becomes more complex, you may want to split it into multiple files instead of adding to an ever
growing `config.yaml` file.

First config file: `imagenet.yaml`:
```yaml
dataset:
  name: imagenet
  path: /datasets/imagenet
```

Second config file: `nesterov.yaml`:
```yaml
optimizer:
  type: nesterov
  lr: 0.001
```

To reduce the number of configuration files scattered in your code directory, you can put them all inside a `conf` subdirectory.

```text
$ tree config_splitting/
config_splitting/
├── conf
│   ├── config.yaml
│   ├── imagenet.yaml
│   └── nesterov.yaml
├── README.md
└── experiment.py
```

For simplicity, we still want our code to operate on a single configuration object.
Add a `defaults` block to the primary config file; config files mentioned there will be loaded and merged automatically.
`config.yaml`:

```yaml
defaults:
  - imagenet
  - nesterov
```

This functionality is similar to an [include directive](https://en.wikipedia.org/wiki/Include_directive), 
but it's actually quite different: The configs are merged into a single object using 
[OmegaConf merge](https://omegaconf.readthedocs.io/en/latest/usage.html#merging-configurations). 

As before, we just tell Hydra what is the name of the main config (except it's now `conf/config.yaml`)
```python
import hydra


@hydra.main(config_path='conf/config.yaml')
def experiment(cfg):
    print(cfg.pretty())


if __name__ == "__main__":
    experiment()
```

Running the app, we get a single config object that combines the input configuration files:
```yaml
$ python experiment.py
dataset:
  name: imagenet
  path: /datasets/imagenet
optimizer:
  lr: 0.001
  type: nesterov
```

Check the [runnable example](https://github.com/facebookresearch/hydra/tree/master/demos/4_config_splitting).