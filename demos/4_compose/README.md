## Composing configuration

A powerful feature of Hydra is that it lets you compose configuration objects dynamically.
This eliminates the need to have 50 modified copies of your master config file, each representing a different variation of your
experiment.

```python
@hydra.main(config_path='conf')
def experiment(cfg):
    print("Configuration:\n{}".format(cfg.pretty()))
```

Note how config_path here is just the path conf (again, relative to the location of the python file you are running).
We will add 6 config files here, so it's nice to put them in a subdirectory and not with the rest of the code.

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

The configuraiton tree contains 3 directories:
 - dataset
 - model
 - optimizer
 
Each is a family of configurations, and we have two of each family.
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
This is the content of conf/dataset/imagenet.yaml!

We can also load one of each:
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
$ python demos/4_compose/compose.py dataset=imagenet optimizer=adam model=resnet dataset.path=/datasets/new-imagenet
Configuration:
dataset:
  name: imagenet
  path: /datasets/new-imagenet
model:
  num_layers: 50
  type: resnet
  width: 10
optimizer:
  beta: 0.01
  lr: 0.1
  type: adam
```

[Prev](../3_config_file/README.md) [Up](../README.md) [Next](../5_defaults/README.md)
