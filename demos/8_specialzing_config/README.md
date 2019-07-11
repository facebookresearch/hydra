# Specializing configuration

In some cases you want to have some default configuration that depends on other configuration choices.
For example, for a specific dataset - you may want to have a specific model by default, or
and maybe for a specific model and dataset you want to have a specific learning rate if the optimizer is Nesterov.

In this demo we will ensure that by default, if we train Alexnet model on Cifar10 dataset, we would automatically change the number of layers from the default of 7 to 5.

You may remember that in the defaults config demo, this is what our config looked like:
```yaml
defaults:
  - dataset: imagenet
  - model: alexnet
```

Now we want to specialize the config based on something that depends on the combination of dataset and model selected.
Furthermore, we only want to do that if right now for dataset=cifar10 and model=alexnet.

The idea is that we can add another element to the defaults list that would load a file name that depends on those two values:
```yaml
defaults:
  - dataset: imagenet
  - model: alexnet
  - dataset_model: ${defaults.0.dataset}_${defaults.1.model}
    optional: true
```

Let's break this down:
##### dataset_model
The key `dataset_model` is an arbitrary directory, it can be anything unique that makes sense, including nested directory like
`dataset/model`.
#### ${defaults.0.dataset}_${defaults.1.model}
the value `${defaults.0.dataset}_${defaults.1.model}` is using OmegaConf's [variable interpolation](https://omegaconf.readthedocs.io/en/latest/usage.html#variable-interpolation).
At runtime, that value would resolve to *imagenet_alexnet*, or *cifar_resent* - depending on the values of defaults.dataset and defaults.model.
This a bit clunky because defaults contains a list (I hope to improve this in the future)
#### optional: true
By default, Hydra would fail with an error if a config specified in the defaults does not exist.
in this case we only want to specialize cifar10 + alexnet, not all 4 combinations.
indication optional: true here tells Hydra to just continue if it can't find this file.

When specializing config, you usually want to only specify what's different, and not the whole thing.
We want the model for alexnet, when trained on cifar - to have 5 layers.

* dataset_model/cifar10_alexnet.yaml*
```yaml
model:
  num_layers: 5
```
 
Let's check. Running with the default uses imagenet, so we don't get the specialized version of:

```yaml
$ python demos/8_specialzing_config/specialize.py 
dataset:
  name: imagenet
  path: /datasets/imagenet
model:
  num_layers: 7
  type: alexnet
```

Running with cifar10 dataset, we do get 5 for num_layers:
```yaml
$ python demos/8_specialzing_config/specialize.py dataset=cifar10
dataset:
  name: cifar10
  path: /datasets/cifar10
model:
  num_layers: 5
  type: alexnet
```



[[Prev](../7_objects)] [[Up](../README.md)]