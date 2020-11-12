---
id: optuna_sweeper
title: Optuna Sweeper plugin
sidebar_label: Optuna Sweeper plugin
---

[![Example application](https://img.shields.io/badge/-Example%20application-informational)](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_optuna_sweeper/example)
[![Plugin source](https://img.shields.io/badge/-Plugin%20source-informational)](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_optuna_sweeper)


This plugin enables Hydra applications to utilize [Optuna](https://optuna.org) for the optimization of the parameters of experiments.

### Installation

```commandline
git clone https://github.com/facebookresearch/hydra.git
cd hydra
pip install plugins/hydra_optuna_sweeper
```

### Usage

Please set `hydra/sweeper` to `optuna` in your config file.

```yaml
defaults:
  - hydra/sweeper: optuna
```

Alternatively, add `hydra/sweeper=optuna` option to your command line.

The default configuration is [here](https://github.com/facebookresearch/hydra/blob/master/plugins/hydra_optuna_sweeper/hydra_plugins/hydra_optuna_sweeper/config.py).

### Example

You can see an example in this directory. `example/sphere.py` implements a simple benchmark function to be minimized.

```commandline
python example/sphere.py --multirun 'x=interval(-5.0, 5.0)' 'y=interval(1, 10)'
```

By default, `interval` is converted to [`UniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.UniformDistribution.html). You can use [`IntUniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntUniformDistribution.html) or [`LogUniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.LogUniformDistribution.html) by specifying the tags:

```commandline
python example/sphere.py --multirun 'x=tag(int, interval(-5.0, 5.0))' 'y=tag(log, interval(1, 10))'
```

The output is as follows:

```commandline
[HYDRA] Study name: sphere
[HYDRA] Storage: None
[HYDRA] Sampler: TPESampler
[HYDRA] Direction: minimize
[HYDRA] Launching 1 jobs locally
[HYDRA]        #0 : x=-3 y=1.6859762540733367
[HYDRA] Launching 1 jobs locally
[HYDRA]        #1 : x=1 y=5.237816870668193
...
[HYDRA] Best parameters: {'x': 0, 'y': 1.0929184723430116}
[HYDRA] Best value: 1.1944707871885822
```

`range` is converted to [`IntUniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntUniformDistribution.html). If you apply `shuffle` to `range`, [`CategoricalDistribution`]((https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.CategoricalDistribution.html)) is used instead.

```commandline
python example/sphere.py --multirun 'x=range(-5.0, 5.0)' 'y=shuffle(range(-5, 5))'
```

The output is as follows:

```commandline
[HYDRA] Study name: sphere
[HYDRA] Storage: None
[HYDRA] Sampler: TPESampler
[HYDRA] Direction: minimize
[HYDRA] Launching 1 jobs locally
[HYDRA]        #0 : x=-3 y=-1
[HYDRA] Launching 1 jobs locally
[HYDRA]        #1 : x=1 y=0
...
[HYDRA] Best parameters: {'x': 1, 'y': 0}
[HYDRA] Best value: 1
```

`choice` is converted to [`CategoricalDistribution`]((https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.CategoricalDistribution.html)).

```commandline
python example/sphere.py --multirun 'x=choice(-5.0, 0.0, 5.0)' 'y=choice(0, 1, 2, 3, 4, 5)'
```

The output is as follows:

```commandline
[HYDRA] Study name: sphere
[HYDRA] Storage: None
[HYDRA] Sampler: TPESampler
[HYDRA] Direction: minimize
[HYDRA] Launching 1 jobs locally
[HYDRA]        #0 : x=5.0 y=5
[HYDRA] Launching 1 jobs locally
[HYDRA]        #1 : x=5.0 y=2
...
[HYDRA] Best parameters: {'x': 0.0, 'y': 0}
[HYDRA] Best value: 0.0
```
