## Default configuration
In the last example we had to specify one of each config family to get everything.
This can get annoying, let's fix it:

```python
@hydra.main(config_path='conf/config.yaml')
def experiment(cfg):
    print("Configuration:\n{}".format(cfg.pretty()))
```
Configuration files will be relative to conf, which is the parent directory of config.yaml.

This is conf/config.yaml:
```yaml
defaults:
  - dataset: imagenet
  - model: alexnet
  - optimizer: nesterov
```

We have a new special section in there called defaults, and it indicates which configurations to load by default.
Note that it's a list, this means it's order sensitive. we will see cases where it comes in handy later.

As expected - running defaults.py without specifying anything will load the defaults:
```yaml
$ python demos/5_defaults/defaults.py
Configuration:
dataset:
  name: imagenet
  path: /datasets/imagenet
model:
  num_layers: 7
  type: alexnet
optimizer:
  lr: 0.001
  type: nesterov
```
 

We can of course still choose to combine different members of each config family:
```text
$ python demos/3_defaults/defaults.py dataset=cifar10
[2019-06-21 20:04:55,590][__main__][INFO] - Configuration:
dataset:
  name: cifar10
  path: /datasets/cifar10
model:
  num_layers: 7
  type: alexnet
optimizer:
  lr: 0.001
  type: nesterov
```

[[Prev](../4_compose)] [[Up](../README.md)] [[Next](../6_sweep)]
