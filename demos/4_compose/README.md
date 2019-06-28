## Composing configuration

A powerful feature of Hydra is that it lets you compose configuration objects dynamically.
This eliminates the need to have 50 modified copies of your master config file, each representing a different variation of your
experiment.

```python
@hydra.main(config_path='conf')
def experiment(cfg):
    print("Configuration:\n{}".format(cfg.pretty()))
```

Note how config_path points to the directory conf. This directory is relative to the python file containing @hydra.main()
This example will use 6 config files, so it's nice to put them in a subdirectory and not with the rest of the code.

The configuraiton tree contains 3 directories:
 - dataset
 - model
 - optimizer

Each is a family of configurations, and we have two of each family:

```text
$ tree demos/4_compose/conf/
demos/4_compose/conf/
├── dataset
│   ├── cifar10.yaml
│   └── imagenet.yaml
├── model
│   ├── alexnet.yaml
│   └── resnet.yaml
└── optimizer
    ├── adam.yaml
    └── nesterov.yaml
```
 
At this point, nothing is loaded by default:
```text
$ python demos/4_compose/compose.py
Configuration:
{}
```

Let's try to compose some configurations:
```yaml
$ python demos/4_compose/compose.py dataset=imagenet
Configuration:
dataset:
  name: imagenet
  path: /datasets/imagenet
```
This is the content of [conf/dataset/imagenet.yaml](conf/dataset/imagenet.yaml)!

We can load at most one config file from each family, let's load exactly one of each:
```yaml
$ python demos/4_compose/compose.py dataset=imagenet optimizer=adam model=resnet
Configuration:
dataset:
  name: imagenet
  path: /datasets/imagenet
model:
  num_layers: 50
  type: resnet
  width: 10
optimizer:
  beta: 0.01
  lr: 0.1
  type: adam
```

It will not surprise you that you can also override the generated config from the command line:
```yaml
$ python demos/4_compose/compose.py dataset=imagenet optimizer=adam dataset.path=/datasets/new-imagenet
Configuration:
dataset:
  name: imagenet
  path: /datasets/new-imagenet
optimizer:
  beta: 0.01
  lr: 0.1
  type: adam
```

[[Prev](../3_config_file)] [[Up](../README.md)] [[Next](../5_defaults)]
