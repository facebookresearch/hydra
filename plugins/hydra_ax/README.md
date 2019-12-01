# Hydra Ax Launcher plugin

This plugin provides a mechanism for Hydra applications to use the [Adaptive Experimentation Platform aka Ax](https://ax.dev/). Ax can be used to optimize any kind of experiment - machine learning experiments, A/B tests and simulations. 

The plugin can be installed by running the following command in the `plugins/hydra_ax` directory:

```
python setup.py install
```

We include an example of how to use this plugin. The file `plugins/hydra_ax/example/banana.py` implements the [Rosenbrock function (aka Banana function)](https://en.wikipedia.org/wiki/Rosenbrock_function). Ax Platform expects two return values from the function (that is being evaluated/optimized) - mean and SEM value. For more details on this, refer the [Ax documentation](https://ax.dev/tutorials/gpei_hartmann_service.html#3.-Define-how-to-evaluate-trials). Since we are using a deterministic function, we invoke the function only once, return the function value as the mean and the SEM value as 0.

To compute the best parameters for the Banana function, run the following command in the plugins/hydra_ax` directory:

```
python example/banana.py -m banana.x=-5.0:5 banana.y=-5:5.0
```

This sets the range if `x` parameter as `[-5, 5]` and the range of `y` parameter as `[-5, 5]`. Other supported formats are fixed parameters (eg `banana.x=5.0`) and choice parameters (eg `banana.x=0,5`).