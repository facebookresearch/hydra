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

```console
python example/sphere.py -m 'x=interval(-5.0, 5.0)' 'y=interval(1, 10)'
```

By default, interval is converted to [`UniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.UniformDistribution.html). You can use [`IntUniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntUniformDistribution.html) or [`LogUniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.LogUniformDistribution.html) by specifying the tags:

```console
python example/sphere.py -m 'x=tag(int, interval(-5.0, 5.0))' 'y=tag(log, interval(1, 10))'
```
