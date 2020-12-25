---
id: specializing_config
title: Specializing configuration
---
[![Example application](https://img.shields.io/badge/-Example%20application-informational)](https://github.com/facebookresearch/hydra/tree/master/examples/patterns/specializing_config)

In some cases the desired configuration should depend on other configuration choices.
For example, You may want to use only 5 layers in your Alexnet model if the dataset of choice is cifar10, and the dafault 7 otherwise.
 
We can start with a config that looks like this:
### initial config.yaml
```yaml
defaults:
  - dataset: imagenet
  - model: alexnet
```

We want to specialize the config based on the choice of the selected dataset and model:
Furthermore, we only want to do it for cifar10 and alexnet and not for 3 other combinations.

OmegaConf supports value interpolation, we can construct a value that would - at runtime - be a function of other values.
The idea is that we can add another element to the defaults list that would load a file name that depends on those two values:
### modified config.yaml
```yaml
defaults:
  - dataset: imagenet
  - model: alexnet
  - optional dataset_model: ${dataset}_${model}
```

Let's break this down:
#### dataset_model
The key `dataset_model` is an arbitrary directory, it can be anything unique that makes sense, including nested directory like `dataset/model`.

#### ${dataset}_${model}
the value `${dataset}_${model}` is using OmegaConf's [variable interpolation](https://omegaconf.readthedocs.io/en/latest/usage.html#variable-interpolation) syntax.
At runtime, that value would resolve to *imagenet_alexnet*, or *cifar_resnet* - depending on the values of defaults.dataset and defaults.model.

:::info
This is not standard interpolations and there are some subtle differences and limitations.
:::


#### optional
By default, Hydra fails with an error if a config specified in the defaults does not exist.
In this case we only want to specialize cifar10 + alexnet, not all 4 combinations.
the keyword `optional` tells Hydra to just continue if it can't find this file.

When specializing config, you usually want to only specify what's different, and not the whole thing.
We want the model for alexnet, when trained on cifar - to have 5 layers.

### dataset_model/cifar10_alexnet.yaml
```yaml
model:
  num_layers: 5
```
 
Let's check. Running with the default uses imagenet, so we don't get the specialized version of:

```yaml
$ python example.py 
dataset:
  name: imagenet
  path: /datasets/imagenet
model:
  num_layers: 7
  type: alexnet
```

Running with cifar10 dataset, we do get 5 for num_layers:
```yaml
$ python example.py dataset=cifar10
dataset:
  name: cifar10
  path: /datasets/cifar10
model:
  num_layers: 5
  type: alexnet
```
