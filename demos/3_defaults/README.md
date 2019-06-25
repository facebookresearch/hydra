## Default configuration
This example re-introduces the config.yaml file, and adds a default section into it that tells
Hydra what to load by default and at what order:

```python
@hydra.main(config_path='conf/config.yaml')
def experiment(cfg):
    ...
```

conf/config.yaml:
```yaml
defaults:
  - dataset: imagenet
  - model: alexnet
  - optimizer: nesterov
```

When we run the new file, it loads all the defaults:
```text
$ python demos/3_defaults/defaults.py
[2019-06-21 20:03:20,049][__main__][INFO] - Running on: devfair0260
[2019-06-21 20:03:20,049][__main__][INFO] - CWD: /private/home/omry/dev/hydra/outputs/2019-06-21_20-03-20
[2019-06-21 20:03:20,050][__main__][INFO] - Configuration:
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
[2019-06-21 20:04:55,589][__main__][INFO] - Running on: devfair0260
[2019-06-21 20:04:55,589][__main__][INFO] - CWD: /private/home/omry/dev/hydra/outputs/2019-06-21_20-04-55
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