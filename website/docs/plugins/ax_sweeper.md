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
This plugin requires Hydra 1.0 (Release candidate)
```commandline
$ pip install hydra-ax-sweeper --pre
```

### Usage
Once installed, add `hydra/sweeper=ax` to your command line. Alternatively, override `hydra/sweeper` in your config:

```yaml
defaults:
  - hydra/sweeper: ax
```

We include an example of how to use this plugin. The file [`example/banana.py`](plugins/hydra_ax/example/banana.py) implements the [Rosenbrock function (aka Banana function)](https://en.wikipedia.org/wiki/Rosenbrock_function). The return value of the function should be the value that we want to optimize.

To compute the best parameters for the Banana function, clone the code and run the following command in the `plugins/hydra_ax_sweeper` directory:

```
python example/banana.py -m banana.x=-5:5 banana.y=-5:10.1
```

The output of a run looks like:

```
[HYDRA] AxSweeper is optimizing the following parameters:
banana.x: range=[-5, 5], type = int
banana.y: range=[-5.0, 10.1], type = float
ax.modelbridge.dispatch_utils: Using Bayesian Optimization generation strategy: GenerationStrategy(name='Sobol+GPEI', steps=[Sobol for 5 arms, GPEI for subsequent arms], generated 0 arm(s) so far). Iterations after 5 will take longer to generate due to model-fitting.
AxSweeper is launching 5 jobs
[HYDRA] Launching 5 jobs locally
[HYDRA] 	#0 : banana.x=4 banana.y=-1.484
[__main__][INFO] - Banana_Function(x=4, y=-1.484)=30581.473
[HYDRA] 	#1 : banana.x=3 banana.y=-3.653
[__main__][INFO] - Banana_Function(x=3, y=-3.653)=16014.261
[HYDRA] 	#2 : banana.x=0 banana.y=9.409
[__main__][INFO] - Banana_Function(x=0, y=9.409)=8855.340
[HYDRA] 	#3 : banana.x=-4 banana.y=2.059
[__main__][INFO] - Banana_Function(x=-4, y=2.059)=19459.063
[HYDRA] 	#4 : banana.x=-3 banana.y=-1.338
[__main__][INFO] - Banana_Function(x=-3, y=-1.338)=10704.497
[HYDRA] New best value: 8855.340, best parameters: {'banana.x': 0, 'banana.y': 9.409}
```

In this example, we set the range of `x` parameter as an integer in `[-5, 5]` and the range of `y` parameter as a float in `[-5, 10.1]`. Note that in the case of `x`, both the upper and the lower range values are integers, and hence only integers are sampled. In the case of `y`, the lower range value is an int while the upper range value is a float. The lower range value is promoted to float as well, and floating-point numbers are sampled from the range. Other supported formats are fixed parameters (eg `banana.x=5.0`) and choice parameters (eg `banana.x=1,2,3`). 

The values of the `x` and `y` parameters can also be set using the config file `plugins/hydra_ax_sweeper/example/conf/config.yaml`. For instance, the configuration corresponding to the parameter `x` is as follows:

```
banana.x:
 type: range
 bounds: [-5, 5]

banana.y:
 type: range
 bounds: [-5, 10.1]
```

The `x` parameter takes on a "range" of integer values, between `-5` to `5`. The `y` parameter takes on a range of floating-point values between `-5` to `10.1`. In general, the plugin supports all the [Parameters](https://ax.dev/api/core.html?highlight=range#module-ax.core.parameter) that Ax supports. According to the [Ax documentation](https://ax.dev/api/service.html#ax.service.ax_client.AxClient.create_experiment), the required elements in the config are:

* `name` - Name of the parameter. It is of type string.
* `type` - Type of the parameter. It can take the following values: `range`, `fixed`, or `choice`.
* `bounds` - Required only for the `range` parameters. It should be a list of two values, with the lower bound first.
* `values` - Required only for the `choice` parameters. It should be a list of values.
* `value` - Required only for the `fixed` parameters. It should be a single value. 

Note that when using the config file, the parameter type (int, float, string, etc.) is set via the [`parameter_type` attribute](https://ax.dev/api/core.html?highlight=range#module-ax.core.parameter). One important thing to note is how mixed types (float + int) are handled. For `y` parameter, the range bounds were set to be `-5` to `10.1`. Both the values were upcasted to a float (irrespective of whether the range was set via the command line or the config file). In case the user provides the `parameter_type` attribute in the config, the attribute is not changed when type casting is done. If the user wants to sample integers in range `-5` to `5`, they need to specify the range as `-5:5` or `[-5, 5]` (in config). If they want to sample floats in range `-5` to `5`, they need to specify the range as `-5.0:5.0` or `[-5.0, 5.0]` (in config). The type casted values, and unchanged attributes are passed to the Ax Client. 

The parameters for the optimization process can also be set in the config file. Specifying the Ax config is optional. The most important parameters are listed below:

```
ax_config:
    experiment:
      # Defaults to minimize, set to false to maximize
      minimize: true

    early_stop:
      # Number of epochs without a significant improvement from
      # the currently known best parameters
      # An Epoch is defined as a batch of trials executed in parallel
      max_epochs_without_improvement: 100

      # An improvement larger than epsilon is considered significant
      epsilon: 0.00001
```
