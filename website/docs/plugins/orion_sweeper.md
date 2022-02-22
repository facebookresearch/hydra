---
id: orion_sweeper
title: Orion Sweeper plugin
sidebar_label: Orion Sweeper plugin
---

import GithubLink,{ExampleGithubLink} from "@site/src/components/GithubLink"


[![PyPi](https://img.shields.io/pypi/v/orion.svg)](https://pypi.python.org/pypi/orion)
[![Python](https://img.shields.io/pypi/pyversions/orion.svg)](https://pypi.python.org/pypi/orion)
[![license](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![DOI](https://zenodo.org/badge/102697867.svg)](https://zenodo.org/badge/latestdoi/102697867)
[![rtfd](https://readthedocs.org/projects/orion/badge/?version=stable)](https://orion.readthedocs.io/en/stable/?badge=stable)
[![codecov](https://codecov.io/gh/Epistimio/orion/branch/master/graph/badge.svg)](https://codecov.io/gh/Epistimio/orion)
[![github-actions](https://github.com/Epistimio/orion/workflows/build/badge.svg?branch=master&event=pull_request)](https://github.com/Epistimio/orion/actions?query=workflow:build+branch:master+event:schedule)


[Oríon](https://orion.readthedocs.io/en/stable/) is an asynchronous framework for black-box function optimization.

Its purpose is to serve as a meta-optimizer for machine learning models and training, as well as a flexible experimentation platform for large scale asynchronous optimization procedures.

Core design value is the minimum disruption of a researcher’s workflow. It allows fast and efficient tuning, providing minimum simple non-intrusive (not even necessary!) helper client interface for a user’s script.


### Installation
```commandline
pip install hydra-orion-sweeper --upgrade
```

### Usage
Once installed, add `hydra/sweeper=orion` to your command. Alternatively, override `hydra/sweeper` in your config:

```yaml
defaults:
  - override hydra/sweeper: orion
```

The default configuration is defined and documented <GithubLink to="plugins/hydra_orion_sweeper/hydra_plugins/hydra_orion_sweeper/config.py">here</GithubLink>.
There are several standard approaches for configuring plugins. Check [this page](../patterns/configuring_plugins.md) for more information.

## Example of training using Orion hyperparameter search

We include an example of how to use this plugin. The file <GithubLink to="plugins/hydra_orion_sweeper/example/my_app.py">example/my_app.py</GithubLink> implements an example of minimizing a (dummy) function using a mixture of continuous and discrete parameters.

You can discover the Orion sweeper parameters with:
```yaml title="$ python your_app hydra/sweeper=orion --cfg hydra -p hydra.sweeper"
# @package hydra.sweeper
_target_: hydra_plugins.hydra_orion_sweeper.orion_sweeper.OrionSweeper
orion:
  name: experiment
  version: '1'
  branching: null
  debug: 'False'
worker:
  n_workers: -1
  pool_size: null
  reservation_timeout: 120
  max_trials: 100
  max_trials_per_worker: 1000000
  max_broken: 3
algorithm:
  type: random
  config:
    seed: 1
storage:
  type: pickledb
  host: database.pkl
parametrization:
  lr: uniform(0, 1)
  opt: choices(['Adam', 'SGD'])
  dropout: uniform(0, 1)
  batch_size: uniform(4, 16, discrete=True)
```

The function decorated with `@hydra.main()` returns a float which we want to minimize, the minimum is 0 and reached for:
```yaml
opt: Adam
lr: 0.12
dropout: 0.33
batch_size: 4
```

To run hyperparameter search and look for the best parameters for this function, clone the code and run the following command in the `plugins/hydra_orion_sweeper` directory:
```bash
python example/my_app.py -m
```

You can also override the search space parametrization:
```bash
python example/my_app.py --multirun opt=Adam,SGD batch_size=4,8,16 \
'lr=tag(log, interval(0.001, 1))' 'dropout=interval(0,1)'
```

The initialization of the sweep and the first 5 evaluations (out of 100) look like this:

```text
[2022-02-22 11:54:01,805][HYDRA] Orion Optimizer {'type': 'random', 'config': {'seed': 1}}
[2022-02-22 11:54:01,806][HYDRA] with parametrization {'batch_size': 'choices([4, 8, 16])', 'batch_size': 'uniform(4, 16, discrete=True)', 'opt': "choices(['Adam', 'SGD'])", 'dropout': 'uniform(0, 1)', 'lr': 'loguniform(0.001, 1.0)'}
[2022-02-22 11:54:03,815][HYDRA] Launching 32 jobs locally
[2022-02-22 12:01:39,585][__main__][INFO] - dummy_training(dropout=0.487, lr=0.783, opt=SGD, batch_size=4) = 0.821
[2022-02-22 12:01:39,585][HYDRA]        #1 : lr=0.00606 dropout=0.5066 opt=SGD batch_size=8
[2022-02-22 12:01:39,654][__main__][INFO] - dummy_training(dropout=0.507, lr=0.006, opt=SGD, batch_size=8) = 4.291
[2022-02-22 12:01:39,654][HYDRA]        #2 : lr=0.05545 dropout=0.6341 opt=SGD batch_size=16
[2022-02-22 12:01:39,722][__main__][INFO] - dummy_training(dropout=0.634, lr=0.055, opt=SGD, batch_size=16) = 12.369
[2022-02-22 12:01:39,722][HYDRA]        #3 : lr=0.01383 dropout=0.7384 opt=SGD batch_size=4
[2022-02-22 12:01:39,791][__main__][INFO] - dummy_training(dropout=0.738, lr=0.014, opt=SGD, batch_size=4) = 0.515
[2022-02-22 12:01:39,791][HYDRA]        #4 : lr=0.6268 dropout=0.3241 opt=Adam batch_size=8
[2022-02-22 12:01:39,891][__main__][INFO] - dummy_training(dropout=0.324, lr=0.627, opt=Adam, batch_size=8) = 5.513
...
[2022-02-22 11:54:20,909][HYDRA] Best parameters: batch_size=4 opt=SGD dropout=0.3259 lr=0.04194
```


and the final 2 evaluations look like this:
```text
[2022-02-22 12:01:54,699][HYDRA]        #126 : lr=0.005244 dropout=0.6714 opt=Adam batch_size=8
[2022-02-22 12:01:54,767][__main__][INFO] - dummy_training(dropout=0.671, lr=0.005, opt=Adam, batch_size=8) = 5.456
[2022-02-22 12:01:54,768][HYDRA]        #127 : lr=0.06152 dropout=0.7459 opt=SGD batch_size=8
[2022-02-22 12:01:54,836][__main__][INFO] - dummy_training(dropout=0.746, lr=0.062, opt=SGD, batch_size=8) = 4.47
...
[2022-02-22 12:01:55,171][HYDRA] Completed trials with results: [Result(name='objective', type='objective', value=5.456156)]
[2022-02-22 12:01:55,183][HYDRA] Completed trials with results: [Result(name='objective', type='objective', value=4.47438)]
[2022-02-22 12:01:55,243][HYDRA] Best parameters: batch_size=4 opt=SGD dropout=0.3483 lr=0.1697
```


The run also creates an `optimization_results.yaml` file in your sweep folder with the parameters recommended by the optimizer:
```yaml
name: orion
trials_completed: 128

best_trials_id: 4ba757a5111baf780fea8c2188f7da7f
best_evaluation: 0.08215999999999998
start_time: '2022-02-22 16:54:01.971501'
finish_time: '2022-02-22 16:54:20.886315'
duration: '0:00:18.914814'

best_evaluated_params:
  batch_size: 4
  opt: Adam
  dropout: 0.3259
  lr: 0.04194

```

## Defining the parameters

Orion supports multiple [research dimension](https://orion.readthedocs.io/en/stable/user/searchspace.html)

* `uniform(low, high)`: sample a value from the uniform distribution
* `loguniform(low, high)`: sample a value from the loguniform distribution
* `normal(loc, scale)`: sample a value from the normal distribution
* `choices(options)`: select among the given value
* `fidelity(low, high, base=2)`: This prior is a special placeholder to define a Fidelity dimension. 
The algorithms will not use this prior to sample, but rather for multi-fidelity optimization. 
For an example of an algorithm using multi-fidelity, 
you can look at the documentation of [ASHA](https://orion.readthedocs.io/en/stable/user/algorithms.html#asha)

Special arguments can also be added to the priors to constraint the sampled values;

* `discrete`: force the sampled value to be an integer
* `default_value`: value to use if the hyperparameter is removed
* `precision`: truncate floats to the given precision to avoid training samples that are too alike
* `shape`: make the parameter returns multiple dimension sample

They can be defined either through config file or commandline override.

### Defining through commandline override

Hydra provides a override parser that support rich syntax. 
More documentation can be found in ([OverrideGrammer/Basic](../advanced/override_grammar/basic.md)) and ([OverrideGrammer/Extended](../advanced/override_grammar/extended.md)). 
We recommend you go through them first before proceeding with this doc.

#### Scalar
```commandline
'key=1,5'                               # Choices
`key="uniform(1, 12)"`                  # Interval are float by default
`key="uniform(1, 8, discrete=True)"`    # Scalar bounds cast to a int
`key="loguniform(1,12)"`                
```

**Note:** When adding overrides through the command line you should be careful with escapting.
Hydra need to receive the space definition as string.


For example, for bash you will need to provide the overrides as below.

```bash
python example/my_app.py -m hydra.sweeper.worker.max_trials=32 hydra.sweeper.worker.n_workers=8 opt='"choices(['Adam', 'SGD'])"' batch_size='"choices([4,8,12,16])"' lr='"loguniform(0.001, 1.0)"' dropout='"uniform(0,1)"'
```

### Defining through config file

```yaml
lr: "uniform(0, 1)"
opt: "choices(['Adam', 'SGD'])"
dropout: "uniform(0, 1)"
batch_size: "uniform(4, 16, discrete=True)"
```
