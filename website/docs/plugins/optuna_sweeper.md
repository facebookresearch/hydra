---
id: optuna_sweeper
title: Optuna Sweeper plugin
sidebar_label: Optuna Sweeper plugin
---

[![PyPI](https://img.shields.io/pypi/v/hydra-optuna-sweeper)](https://img.shields.io/pypi/v/hydra-optuna-sweeper)
![PyPI - License](https://img.shields.io/pypi/l/hydra-optuna-sweeper)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hydra-optuna-sweeper)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/hydra-optuna-sweeper.svg)](https://pypistats.org/packages/hydra-optuna-sweeper)
[![Example application](https://img.shields.io/badge/-Example%20application-informational)](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_optuna_sweeper/example)
[![Plugin source](https://img.shields.io/badge/-Plugin%20source-informational)](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_optuna_sweeper)


This plugin enables Hydra applications to utilize [Optuna](https://optuna.org) for the optimization of the parameters of experiments.

## Installation

```commandline
pip install hydra-optuna-sweeper --upgrade
```

## Usage

Please set `hydra/sweeper` to `optuna` in your config file.

```yaml
defaults:
  - override hydra/sweeper: optuna
```

Alternatively, add `hydra/sweeper=optuna` option to your command line.

The default configuration is [here](https://github.com/facebookresearch/hydra/blob/master/plugins/hydra_optuna_sweeper/hydra_plugins/hydra_optuna_sweeper/config.py).

## Example

We include an example in this directory. `example/sphere.py` implements a simple benchmark function to be minimized.

You can discover the Optuna sweeper parameters with:

```yaml title="python example/sphere.py hydra/sweeper=optuna --cfg hydra -p hydra.sweeper"
# @package hydra.sweeper
_target_: hydra_plugins.hydra_optuna_sweeper.optuna_sweeper.OptunaSweeper
optuna_config:
  direction: minimize
  storage: null
  study_name: sphere
  n_trials: 20
  n_jobs: 1
  sampler: TPESampler
  seed: 123
search_space:
  x:
    type: float
    low: -5.5
    high: 5.5
    step: 0.5
  y:
    type: categorical
    choices:
    - -5
    - 0
    - 5
```

The function decorated with `@hydra.main()` returns a float which we want to minimize, the minimum is 0 and reached for:
```yaml
x: 0
y: 0
```

To run optimization, clone the code and run the following command in the `plugins/hydra_optuna_sweeper` directory:

```commandline
python example/sphere.py --multirun
```

You can also override the search space parametrization:

```commandline
python example/sphere.py --multirun 'x=interval(-5.0, 5.0)' 'y=interval(0, 10)'
```

## Search space configuration

This plugin supports Optuna's [distributions](https://optuna.readthedocs.io/en/stable/reference/distributions.html) to configure search spaces. They can be defined either through commandline override or config file.

### Configuring through commandline override

Hydra provides a override parser that support rich syntax. Please refer to [OverrideGrammer/Basic](../advanced/override_grammar/basic.md) and [OverrideGrammer/Extended](../advanced/override_grammar/extended.md) for details.

#### Interval override

By default, `interval` is converted to [`UniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.UniformDistribution.html). You can use [`IntUniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntUniformDistribution.html), [`LogUniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.LogUniformDistribution.html) or [`IntLogUniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntLogUniformDistribution.html) by casting the interval to `int` and tagging it with `log`.

<details><summary>Example for interval override</summary>

```commandline
python example/sphere.py --multirun 'x=int(interval(-5.0, 5.0))' 'y=tag(log, interval(1, 10))'
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

</details>

#### Range override

`range` is converted to [`IntUniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntUniformDistribution.html). If you apply `shuffle` to `range`, [`CategoricalDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.CategoricalDistribution.html) is used instead.

<details><summary>Example for range override</summary>

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

</details>

#### Choice override

`choice` is converted to [`CategoricalDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.CategoricalDistribution.html).

<details><summary>Example for choice override</summary>

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

</details>

### Configuring through config file

#### Int parameters

`int` parameters can be defined with the following fields:

- `type`: `int`
- `low`: lower bound
- `high`: upper bound
- `step`: discretization step (optional)
- `log`: if `true`, space is converted to the log domain

If `log` is `false`, the parameter is mapped to [`IntUniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntUniformDistribution.html). Otherwise, the parameter is mapped to [`IntLogUniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntLogUniformDistribution.html). Please note that `step` can not be set if `log=true`.

#### Float parameters

`float` parameters can be defined with the following fields:

- `type`: `float`
- `low`: lower bound
- `high`: upper bound
- `step`: discretization step
- `log`: if `true`, space is converted to the log domain

If `log` is `false`, the parameter is mapped to [`UniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.UniformDistribution.html) or [`DiscreteUniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.DiscreteUniformDistribution.html) depending on the presence or absence of the `step` field, respectively. Otherwise, the parameter is mapped to [`LogUniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.LogUniformDistribution.html). Please note that `step` can not be set if `log=true`.

#### Categorical parameters

`categorical` parameters can be defined with the following fields:

  - `type`: `categorical`
  - `choices`: a list of parameter value candidates

The parameters are mapped to [`CategoricalDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.CategoricalDistribution.html).
