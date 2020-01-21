# Hydra Ax Launcher plugin

This plugin provides a mechanism for Hydra applications to use the [Adaptive Experimentation Platform, aka Ax](https://ax.dev/). Ax can optimize any experiment - machine learning experiments, A/B tests, and simulations. 

Run the following command to install the plugin:

```
pip install hydra_ax_sweeper
```

We include an example of how to use this plugin. The file [`plugins/hydra_ax_sweeper/example/banana.py`](plugins/hydra_ax/example/banana.py) implements the [Rosenbrock function (aka Banana function)](https://en.wikipedia.org/wiki/Rosenbrock_function). The return value of the function should be the value that we want to optimize.

To compute the best parameters for the Banana function, clone the code and run the following command in the `plugins/hydra_ax_sweeper` directory:

```
python example/banana.py -m banana.x=-5:5 banana.y=-5:10.1
```

This sets the range of `x` parameter as `[-5, 5]` and the range of `y` parameter as `[-5, 10.1]`. Other supported formats are fixed parameters (eg `banana.x=5.0`) and choice parameters (eg `banana.x=1,2,3`). The values of the `x` and `y` parameters can also be set using the config file in `plugins/hydra_ax_sweeper/example/conf/config.yaml`. For instance, the configuration corresponding to the parameter `x` is as follows:

```
banana.x:
 type: range
 bounds: [-5.0, 10.0]
 log_scale: false
```

The `x` parameter takes on a "range" of values, between `-5.0` to `10.0`,  and the values should not be sampled from the log-space. In general, the plugin supports all the [Parameters](https://ax.dev/api/core.html?highlight=range#module-ax.core.parameter) that Ax supports. The required elements in the config are:

* `name` - Name of the parameter. It is of type string.
* `type` - Type of the parameter. It can take the following values: `range`, `fixed`, or `choice`.
* `bounds` - Required only for the `range` parameters. It should be a list of two values, with the lower bound first.
* `values` - Required only for the `choice` parameters. It should be a list of values.
* `value` - Required only for the `fixed` parameters. It should be a single value. 