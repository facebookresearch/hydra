---
id: optuna_sweeper
title: Optuna Sweeper plugin
sidebar_label: Optuna Sweeper plugin
---

import GithubLink,{ExampleGithubLink} from "@site/src/components/GithubLink"

[![PyPI](https://img.shields.io/pypi/v/hydra-optuna-sweeper)](https://pypi.org/project/hydra-optuna-sweeper/)
![PyPI - License](https://img.shields.io/pypi/l/hydra-optuna-sweeper)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hydra-optuna-sweeper)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/hydra-optuna-sweeper.svg)](https://pypistats.org/packages/hydra-optuna-sweeper)<ExampleGithubLink text="Example application" to="plugins/hydra_optuna_sweeper/example"/><ExampleGithubLink text="Plugin source" to="plugins/hydra_optuna_sweeper"/>


This plugin enables Hydra applications to utilize [Optuna](https://optuna.org) for the optimization of the parameters of experiments.

## Installation

This plugin requires `hydra-core>=1.1.0`. Please install it with the following command:

```commandline
pip install hydra-core --upgrade
```

You can install the plugin via pip:

```commandline
pip install hydra-optuna-sweeper --upgrade
```
There are several standard approaches for configuring plugins. Check [this page](../patterns/configuring_plugins.md) for more information.

## Usage

Please set `hydra/sweeper` to `optuna` in your config file.

```yaml
defaults:
  - override hydra/sweeper: optuna
```

Alternatively, add `hydra/sweeper=optuna` option to your command line.

The default configuration is <GithubLink to="plugins/hydra_optuna_sweeper/hydra_plugins/hydra_optuna_sweeper/config.py">here</GithubLink>.

## Example 1: Single-Objective Optimization

We include an example in <GithubLink to="plugins/hydra_optuna_sweeper/example">this directory</GithubLink>. `example/sphere.py` implements a simple benchmark function to be minimized.

You can discover the Optuna sweeper parameters with:

```yaml title="python example/sphere.py hydra/sweeper=optuna --cfg hydra -p hydra.sweeper"
# @package hydra.sweeper
sampler:
  _target_: optuna.samplers.TPESampler
  seed: 123
  consider_prior: true
  prior_weight: 1.0
  consider_magic_clip: true
  consider_endpoints: false
  n_startup_trials: 10
  n_ei_candidates: 24
  multivariate: false
  warn_independent_sampling: true
_target_: hydra_plugins.hydra_optuna_sweeper.optuna_sweeper.OptunaSweeper
direction: minimize
storage: null
study_name: sphere
n_trials: 20
n_jobs: 1
search_space:
  x:
    type: float
    low: -5.5
    high: 5.5
    step: 0.5
  'y':
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

You might find the `optimization_results.yaml` file (i.e. best params and best value) under `multirun` logs folder:

```yaml
name: optuna
best_params:
  x: 0.0
  'y': 0
best_value: 0.0
```


## Sampler configuration
This plugin supports Optuna's [samplers](https://optuna.readthedocs.io/en/stable/reference/samplers.html).
You can change the sampler by overriding `hydra/sweeper/sampler` or change sampler settings within `hydra.sweeper.sampler`.

## Search space configuration

This plugin supports Optuna's [distributions](https://optuna.readthedocs.io/en/stable/reference/distributions.html) to configure search spaces. They can be defined either through commandline override or config file.

### Configuring through commandline override

Hydra provides a override parser that support rich syntax. Please refer to [OverrideGrammer/Basic](../advanced/override_grammar/basic.md) and [OverrideGrammer/Extended](../advanced/override_grammar/extended.md) for details.

#### Interval override

By default, `interval` is converted to [`UniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.UniformDistribution.html). You can use [`IntUniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntUniformDistribution.html), [`LogUniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.LogUniformDistribution.html) or [`IntLogUniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntLogUniformDistribution.html) by casting the interval to `int` and tagging it with `log`.

<details>
  <summary>Example for interval override</summary>

  ```commandline
  python example/sphere.py --multirun 'x=int(interval(-5.0, 5.0))' 'y=tag(log, interval(1, 10))'
  ```

  The output is as follows:

  ```commandline
  [HYDRA] Study name: sphere
  [HYDRA] Storage: None
  [HYDRA] Sampler: TPESampler
  [HYDRA] Directions: ['minimize']
  [HYDRA] Launching 1 jobs locally
  [HYDRA] 	#0 : x=-3 y=1.6859762540733367
  [HYDRA] Launching 1 jobs locally
  [HYDRA] 	#1 : x=1 y=5.237816870668193
  ...
  [HYDRA] Best parameters: {'x': 0, 'y': 1.0929184723430116}
  [HYDRA] Best value: 1.1944707871885822
  ```

</details>

#### Range override

`range` is converted to [`IntUniformDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntUniformDistribution.html). If you apply `shuffle` to `range`, [`CategoricalDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.CategoricalDistribution.html) is used instead.

<details>
  <summary>Example for range override</summary>

  ```commandline
  python example/sphere.py --multirun 'x=range(-5.0, 5.0)' 'y=shuffle(range(-5, 5))'
  ```

  The output is as follows:

  ```commandline
  [HYDRA] Study name: sphere
  [HYDRA] Storage: None
  [HYDRA] Sampler: TPESampler
  [HYDRA] Directions: ['minimize']
  [HYDRA] Launching 1 jobs locally
  [HYDRA] 	#0 : x=-3 y=-4
  [HYDRA] Launching 1 jobs locally
  [HYDRA] 	#1 : x=1 y=-1
  ...
  [HYDRA] Best parameters: {'x': 0, 'y': -1}
  [HYDRA] Best value: 1.0
  ```

</details>

#### Choice override

`choice` is converted to [`CategoricalDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.CategoricalDistribution.html).

<details>
  <summary>Example for choice override</summary>

  ```commandline
  python example/sphere.py --multirun 'x=choice(-5.0, 0.0, 5.0)' 'y=choice(0, 1, 2, 3, 4, 5)'
  ```

  The output is as follows:

  ```commandline
  [HYDRA] Study name: sphere
  [HYDRA] Storage: None
  [HYDRA] Sampler: TPESampler
  [HYDRA] Directions: ['minimize']
  [HYDRA] Launching 1 jobs locally
  [HYDRA] 	#0 : x=5.0 y=5
  [HYDRA] Launching 1 jobs locally
  [HYDRA] 	#1 : x=5.0 y=2
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


## Example 2:  Multi-Objective Optimization

In the same directory, `example/multi-objective.py` implements a simple benchmark function, which has two objective values. We want to minimize two objectives simultaneously.

You can discover the Optuna sweeper parameters with:

```commandline
python example/multi-objective.py hydra/sweeper=optuna --cfg hydra -p hydra.sweeper
```

<details>
  <summary>Configuration of the multi-objective optimization example</summary>

  ```yaml
  # @package hydra.sweeper
  sampler:
    _target_: optuna.samplers.NSGAIISampler
    seed: 123
    population_size: 50
    mutation_prob: null
    crossover_prob: 0.9
    swapping_prob: 0.5
    constraints_func: null
  _target_: hydra_plugins.hydra_optuna_sweeper.optuna_sweeper.OptunaSweeper
  direction:
  - minimize
  - minimize
  storage: null
  study_name: multi-objective
  n_trials: 20
  n_jobs: 1
  search_space:
    x:
      type: float
      low: 0
      high: 5
      step: 0.5
    'y':
      type: float
      low: 0
      high: 3
      step: 0.5
  ```
</details>


To run the optimization, use the following command in the `plugins/hydra_optuna_sweeper` directory:

```commandline
python example/multi-objective.py --multirun
```

For problems with trade-offs between two different objectives, there may be no single solution that simultaneously minimizes both objectives. Instead, we obtained a set of solutions, namely [Pareto optimal solutions](https://en.wikipedia.org/wiki/Pareto_efficiency), that show the best trade-offs possible between the objectives. In the following figure, the blue dots show the Pareto optimal solutions in the optimization results.

![Pareto-optimal solutions](/plugins/optuna_sweeper/multi_objective_result.png)
