---
id: nevergrad_sweeper
title: Nevergrad Sweeper plugin
sidebar_label: Nevergrad Sweeper plugin
---

[![PyPI](https://img.shields.io/pypi/v/hydra-nevergrad-sweeper)](https://pypi.org/project/hydra-nevergrad-sweeper/)
![PyPI - License](https://img.shields.io/pypi/l/hydra-nevergrad-sweeper)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hydra-nevergrad-sweeper)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/hydra-nevergrad-sweeper.svg)](https://pypistats.org/packages/hydra-nevergrad-sweeper)
[![Example application](https://img.shields.io/badge/-Example%20application-informational)](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_nevergrad_sweeper/example)
[![Plugin source](https://img.shields.io/badge/-Plugin%20source-informational)](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_nevergrad_sweeper)


[Nevergrad](https://facebookresearch.github.io/nevergrad/) is a derivative-free optimization platform providing a library of state-of-the-art algorithms for hyperparameter search. This plugin provides Hydra applications a mechanism to use [Nevergrad](https://facebookresearch.github.io/nevergrad/) algorithms to optimize experiment/application parameters.

### Installation
```commandline
pip install hydra-nevergrad-sweeper --upgrade
```

### Usage
Once installed, add `hydra/sweeper=nevergrad` to your command. Alternatively, override `hydra/sweeper` in your config:

```yaml
defaults:
  - override hydra/sweeper: nevergrad
```


The default configuration is [here](https://github.com/facebookresearch/hydra/blob/master/plugins/hydra_nevergrad_sweeper/hydra_plugins/hydra_nevergrad_sweeper/config.py).

## Example of training using Nevergrad hyperparameter search

We include an example of how to use this plugin. The file [`example/my_app.py`](https://github.com/facebookresearch/hydra/blob/master/plugins/hydra_nevergrad_sweeper/example/my_app.py) implements an example of minimizing a (dummy) function using a mixture of continuous and discrete parameters.

You can discover the Nevergrad sweeper parameters with:
```yaml title="$ python your_app hydra/sweeper=nevergrad --cfg hydra -p hydra.sweeper"
# @package hydra.sweeper
_target_: hydra_plugins.hydra_nevergrad_sweeper.core.NevergradSweeper
optim:
  optimizer: OnePlusOne
  budget: 80
  num_workers: 10
  noisy: false
  maximize: false
  seed: null
parametrization: {}
version: 1
```

The function decorated with `@hydra.main()` returns a float which we want to minimize, the minimum is 0 and reached for:
```yaml
db: mnist
lr: 0.12
dropout: 0.33
batch_size=4
```

To run hyperparameter search and look for the best parameters for this function, clone the code and run the following command in the `plugins/hydra_nevergrad_sweeper` directory:
```bash
python example/my_app.py -m
```

You can also override the search space parametrization:
```bash
python example/my_app.py --multirun db=mnist,cifar batch_size=4,8,16 \
'lr=tag(log, interval(0.001, 1))' 'dropout=interval(0,1)'
```

The initialization of the sweep and the first 5 evaluations (out of 100) look like this:

```text
[2020-10-08 20:13:53,592][HYDRA] NevergradSweeper(optimizer=OnePlusOne, budget=100, num_workers=10) minimization
[2020-10-08 20:13:53,593][HYDRA] with parametrization Dict(batch_size=Choice(choices=Tuple(4,8,16),weights=Array{(1,3)}),db=Choice(choices=Tuple(mnist,cifar),weights=Array{(1,2)}),dropout=Scalar{Cl(0,1,b)}[sigma=Log{exp=2.0}],lr=Log{exp=3.162277660168379,Cl(0.001,1,b)}):{'db': 'mnist', 'lr': 0.03162277660168379, 'dropout': 0.5, 'batch_size': 8}
[2020-10-08 20:13:53,593][HYDRA] Sweep output dir: multirun/2020-10-08/20-13-53
[2020-10-08 20:13:55,023][HYDRA] Launching 10 jobs locally
[2020-10-08 20:13:55,023][HYDRA]        #0 : db=mnist lr=0.03162277660168379 dropout=0.5 batch_size=16
[2020-10-08 20:13:55,217][__main__][INFO] - dummy_training(dropout=0.500, lr=0.032, db=mnist, batch_size=16) = 13.258
[2020-10-08 20:13:55,218][HYDRA]        #1 : db=cifar lr=0.018178519762066934 dropout=0.5061074452336254 batch_size=4
[2020-10-08 20:13:55,408][__main__][INFO] - dummy_training(dropout=0.506, lr=0.018, db=cifar, batch_size=4) = 0.278
[2020-10-08 20:13:55,409][HYDRA]        #2 : db=cifar lr=0.10056825918734161 dropout=0.6399687427725211 batch_size=4
[2020-10-08 20:13:55,595][__main__][INFO] - dummy_training(dropout=0.640, lr=0.101, db=cifar, batch_size=4) = 0.329
[2020-10-08 20:13:55,596][HYDRA]        #3 : db=mnist lr=0.06617542958182834 dropout=0.5059497416026679 batch_size=8
[2020-10-08 20:13:55,812][__main__][INFO] - dummy_training(dropout=0.506, lr=0.066, db=mnist, batch_size=8) = 5.230
[2020-10-08 20:13:55,813][HYDRA]        #4 : db=mnist lr=0.16717013388679514 dropout=0.6519070394318255 batch_size=4
...
[2020-10-08 20:14:27,988][HYDRA] Best parameters: db=cifar lr=0.11961221693764439 dropout=0.37285878409770895 batch_size=4
```


and the final 2 evaluations look like this:
```text
[HYDRA] 	#8 : db=mnist batch_size=4 lr=0.094 dropout=0.381
[__main__][INFO] - my_app.py(dropout=0.381, lr=0.094, db=mnist, batch_size=4) = 1.077
[HYDRA] 	#9 : db=mnist batch_size=4 lr=0.094 dropout=0.381
[__main__][INFO] - my_app.py(dropout=0.381, lr=0.094, db=mnist, batch_size=4) = 1.077
[HYDRA] Best parameters: db=mnist batch_size=4 lr=0.094 dropout=0.381
```


The run also creates an `optimization_results.yaml` file in your sweep folder with the parameters recommended by the optimizer:
```yaml
best_evaluated_result: 0.381

best_evaluated_params:
  batch_size: 4
  db: mnist
  dropout: 0.381
  lr: 0.094

name: nevergrad
```

## Defining the parameters

The plugin supports two types of parameters: [Choices](https://facebookresearch.github.io/nevergrad/parametrization_ref.html#nevergrad.p.Choice) and [Scalars](https://facebookresearch.github.io/nevergrad/parametrization_ref.html#nevergrad.p.Scalar). They can be defined either through config file or commandline override.

### Defining through commandline override
Hydra provides a override parser that support rich syntax. More documentation can be found in ([OverrideGrammer/Basic](../advanced/override_grammar/basic.md)) and ([OverrideGrammer/Extended](../advanced/override_grammar/extended.md)). We recommend you go through them first before proceeding with this doc.

#### Choices
To override a field with choices:
```commandline
'key=1,5'
'key=shuffle(range(1, 8))'
'key=range(1,5)'
```

You can tag an override with ```ordered``` to indicate it's a [```TransitionChoice```](https://facebookresearch.github.io/nevergrad/parametrization_ref.html#nevergrad.p.TransitionChoice)
```commandline
`key=tag(ordered, choice(1,2,3))`
```

#### Scalar
```commandline
`key=interval(1,12)`             # Interval are float by default
`key=int(interval(1,8))`         # Scalar bounds cast to a int
`key=tag(log, interval(1,12))`   # call ng.p.Log if tagged with log
```

### Defining through config file
#### Choices
Choices are defined with a list in a config file.

```yaml
db:
  - mnist
  - cifar
```
#### Scalars
Scalars can be defined in config files, with fields:
  - `init`: optional initial value
  - `lower` : optional lower bound
  - `upper`: optional upper bound
  - `log`: set to `true` for log distributed values
  - `step`: optional step size for looking for better parameters. In linear mode, this is an additive step; in logarithmic mode it is multiplicative.
  - `integer`: set to `true` for integers (favor floats over integers whenever possible)

Providing only `lower` and `upper` bound will set the initial value to the middle of the range and the step to a sixth of the range.
**Note**: unbounded scalars (scalars with no upper and/or lower bounds) can only be defined through a config file.