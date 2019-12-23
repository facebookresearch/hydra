# Hydra Ax Launcher plugin

This plugin provides a mechanism for Hydra applications to use the [Adaptive Experimentation Platform aka Ax](https://ax.dev/). Ax can be used to optimize any kind of experiment - machine learning experiments, A/B tests, and simulations. 

The plugin can be installed by running the following command:

```
pip install hydra-ax
```

We include an example of how to use this plugin. The file [`plugins/hydra_ax/example/banana.py`](plugins/hydra_ax/example/banana.py) implements the [Rosenbrock function (aka Banana function)](https://en.wikipedia.org/wiki/Rosenbrock_function). The return value of the function should be the value that we want to optimize.

To compute the best parameters for the Banana function, clone the code and run the following command in the `plugins/hydra_ax` directory:

```
python example/banana.py -m banana.x=-5:5 banana.y=-5:10.1
```

This sets the range of `x` parameter as `[-5, 5]` and the range of `y` parameter as `[-5, 10.1]`. Other supported formats are fixed parameters (eg `banana.x=5.0`) and choice parameters (eg `banana.x=1,2,3`).