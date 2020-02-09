---
id: ax_sweeper
title: Ax Sweeper plugin
sidebar_label: Ax Sweeper plugin
---
This plugin provides a mechanism for Hydra applications to use the <a class="external" href="https://ax.dev/" target="_blank">Adaptive Experimentation Platform, aka Ax</a>. Ax can optimize any experiment - machine learning experiments, A/B tests, and simulations.

Install with 
```
pip install hydra_ax_sweeper
```

Once installed, override `hydra/sweeper` in your config:

```yaml
defaults:
  - hydra/sweeper: ax
```

and add a config corresponding to all the parameters that you want to optimize. For instance, the configuration corresponding to a parameter `x` may look like this:

```
x:
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

See included [example](https://github.com/facebookresearch/hydra/tree/0.11_branch/plugins/hydra_ax_sweeper/example).
 
Output of a run looks like:

```
[2020-02-09 14:53:07,282][HYDRA] AxSweeper is launching 5 jobs
[2020-02-09 14:53:07,287][HYDRA] Launching 5 jobs locally
[2020-02-09 14:53:07,287][HYDRA] 	#0 : banana.x=4 banana.y=9.366917353868484
[2020-02-09 14:53:07,444][__main__][INFO] - Banana_Function(x=4, y=9.366917353868484)=52.997785390411075
[2020-02-09 14:53:07,447][HYDRA] 	#1 : banana.x=3 banana.y=4.2380884230136875
[2020-02-09 14:53:07,590][__main__][INFO] - Banana_Function(x=3, y=4.2380884230136875)=26.67580186703627
[2020-02-09 14:53:07,592][HYDRA] 	#2 : banana.x=2 banana.y=2.807121509313583
[2020-02-09 14:53:07,736][__main__][INFO] - Banana_Function(x=2, y=2.807121509313583)=2.4229590935423047
[2020-02-09 14:53:07,738][HYDRA] 	#3 : banana.x=1 banana.y=1.6320534139871592
[2020-02-09 14:53:07,886][__main__][INFO] - Banana_Function(x=1, y=1.6320534139871592)=0.39949151813282324
[2020-02-09 14:53:07,888][HYDRA] 	#4 : banana.x=2 banana.y=-1.5182482689619063
[2020-02-09 14:53:08,039][__main__][INFO] - Banana_Function(x=2, y=-1.5182482689619063)=31.45106395790108
[2020-02-09 14:53:08,112][HYDRA] New best value: 0.39949151813282324, best parameters: {'banana.x': 1, 'banana.y': 1.6320534139871592}
```