---
id: ax_sweeper
title: Ax Sweeper plugin
sidebar_label: Ax Sweeper plugin
---
[![PyPI](https://img.shields.io/pypi/v/hydra-ax-sweeper)](https://img.shields.io/pypi/v/hydra-ax-sweeper)
![PyPI - License](https://img.shields.io/pypi/l/hydra-ax-sweeper)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hydra-ax-sweeper)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/hydra-ax-sweeper.svg)](https://pypistats.org/packages/hydra-ax-sweeper)
[![Example application](https://img.shields.io/badge/-Example%20application-informational)](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_ax_sweeper/example)
[![Plugin source](https://img.shields.io/badge/-Plugin%20source-informational)](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_ax_sweeper)

This plugin provides a mechanism for Hydra applications to use the [Adaptive Experimentation Platform, aka Ax](https://ax.dev/). Ax can optimize any experiment - machine learning experiments, A/B tests, and simulations. 

### Installation
```commandline
pip install hydra-ax-sweeper --upgrade
```

### Usage
Once installed, add `hydra/sweeper=ax` to your command line. Alternatively, override `hydra/sweeper` in your config:

```yaml
defaults:
  - hydra/sweeper: ax
    override: true
```

We include an example of how to use this plugin. The file [`example/banana.py`](https://github.com/facebookresearch/hydra/blob/master/plugins/hydra_ax_sweeper/example/banana.py) implements the [Rosenbrock function (aka Banana function)](https://en.wikipedia.org/wiki/Rosenbrock_function). The return value of the function should be the value that we want to optimize.

To compute the best parameters for the Banana function, clone the code and run the following command in the `plugins/hydra_ax_sweeper` directory:

```
python example/banana.py -m 'banana.x=int(interval(-5, 5))' 'banana.y=interval(-5, 10.1)'
```

The output of a run looks like:

```
[HYDRA] AxSweeper is optimizing the following parameters:
banana.x: range=[-5, 5], type = int
banana.y: range=[-5.0, 10.1], type = float
ax.modelbridge.dispatch_utils: Using Bayesian Optimization generation strategy: GenerationStrategy(name='Sobol+GPEI', steps=[Sobol for 5 arms, GPEI for subsequent arms], generated 0 arm(s) so far). Iterations after 5 will take longer to generate due to model-fitting.
AxSweeper is launching 5 jobs
[HYDRA] Launching 5 jobs locally
[HYDRA]   #0 : banana.x=4 banana.y=-1.484
[__main__][INFO] - Banana_Function(x=4, y=-1.484)=30581.473
[HYDRA]   #1 : banana.x=3 banana.y=-3.653
[__main__][INFO] - Banana_Function(x=3, y=-3.653)=16014.261
[HYDRA]   #2 : banana.x=0 banana.y=9.409
[__main__][INFO] - Banana_Function(x=0, y=9.409)=8855.340
[HYDRA]   #3 : banana.x=-4 banana.y=2.059
[__main__][INFO] - Banana_Function(x=-4, y=2.059)=19459.063
[HYDRA]   #4 : banana.x=-3 banana.y=-1.338
[__main__][INFO] - Banana_Function(x=-3, y=-1.338)=10704.497
[HYDRA] New best value: 8855.340, best parameters: {'banana.x': 0, 'banana.y': 9.409}
```

In this example, we set the range of `x` parameter as an integer in the interval `[-5, 5]` and the range of `y` parameter as a float in the interval `[-5, 10.1]`. Note that in the case of `x`, we used `int(interval(...))` and hence only integers are sampled. In the case of `y`, we used `interval(...)` which refers to a floating-point interval. Other supported formats are fixed parameters (e.g.` banana.x=5.0`), choice parameters (eg `banana.x=choice(1,2,3)`) and range (eg `banana.x=range(1, 10)`). Note that `interval`, `choice` etc. are functions provided by Hydra, and you can read more about them [here](https://hydra.cc/docs/next/advanced/override_grammar/extended/). An important thing to remember is, use [`interval`](https://hydra.cc/docs/next/advanced/override_grammar/extended/#interval-sweep) when we want Ax to sample values from an interval. [`RangeParameter`](https://ax.dev/api/ax.html#ax.RangeParameter) in Ax is equivalent to `interval` in Hydra. Remember to use `int(interval(...))` if you want to sample only integer points from the interval. [`range`](https://hydra.cc/docs/next/advanced/override_grammar/extended/#range-sweep) can be used as an alternate way of specifying choice parameters. For example `python example/banana.py -m banana.x=choice(1, 2, 3, 4)` is equivalent to `python example/banana.py -m banana.x=range(1, 5)`.


The values of the `x` and `y` parameters can also be set using the config file `plugins/hydra_ax_sweeper/example/conf/config.yaml`. For instance, the configuration corresponding to the commandline arguments is as follows:

```
banana.x:
 type: range
 bounds: [-5, 5]

banana.y:
 type: range
 bounds: [-5, 10.1]
```

In general, the plugin supports setting all the Ax supported [Parameters](https://ax.dev/api/core.html?highlight=range#module-ax.core.parameter) in the config. According to the [Ax documentation](https://ax.dev/api/service.html#ax.service.ax_client.AxClient.create_experiment), the required elements in the config are:

* `name` - Name of the parameter. It is of type string.
* `type` - Type of the parameter. It can take the following values: `range`, `fixed`, or `choice`.
* `bounds` - Required only for the `range` parameters. It should be a list of two values, with the lower bound first.
* `values` - Required only for the `choice` parameters. It should be a list of values.
* `value` - Required only for the `fixed` parameters. It should be a single value. 

Note that if you want to sample integers in the range `-5` to `5`, you need to specify the range as `int(interval(-5, 5))` (in the command line) or `[-5, 5]` (in config). If you want to sample floats in range `-5` to `5`, you need to specify the range as `interval(-5, 5)` (in the command line) or `[-5.0, 5.0]` (in config).

The parameters for the optimization process can also be set in the config file. Specifying the Ax config is optional. You can discover the Ax Sweeper parameters with:

```yaml title="$ python your_app.py hydra/sweeper=ax --cfg hydra -p hydra.sweeper"
# @package hydra.sweeper
_target_: hydra_plugins.hydra_ax_sweeper.ax_sweeper.AxSweeper
max_batch_size: null
ax_config:
  max_trials: 10
  early_stop:
    minimize: true
    max_epochs_without_improvement: 10
    epsilon: 1.0e-05
  experiment:
    name: null
    objective_name: objective
    minimize: true
    parameter_constraints: null
    outcome_constraints: null
    status_quo: null
  client:
    verbose_logging: false
    random_seed: null
  params: {}
```
