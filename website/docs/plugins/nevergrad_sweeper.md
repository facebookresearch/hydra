---
id: nevergrad_sweeper
title: Nevergrad Sweeper plugin
sidebar_label: Nevergrad Sweeper plugin
---
This plugin provides a mechanism for Hydra applications to use [Nevergrad](https://github.com/facebookresearch/nevergrad) algorithms for the optimization of the parameters of any experiment.

Install with:

```
pip install hydra_nevergrad_sweeper
```

Once installed, override `hydra/sweeper` in your config:

```yaml
defaults:
  - hydra/sweeper: nevergrad
```

We include an example of how to use this plugin. The file [`example/dummy_training.py`](plugins/hydra_nevergrad_sweeper/example/dummy_training.py) implements an example of how to perform minimization of a (dummy) function including a mixture of continuous and discrete parameters. 

To compute the best parameters for this function, clone the code and run the following command in the `plugins/hydra_nevergrad_sweeper` directory:

```
python example/dummy_training.py -m db=mnist,cifar batch_size=4,8,16 lr='Log(a_min=0.001,a_max=1.0)' dropout=0.0:1.0
```

The output of a run looks like:

```
TODO
```

In this example, we set the range of



# About integers and floats

One important thing to note is how float and integers are interpreted in the commandline. When at least one of variable bounds is a float then the parameter is considered to be a float and be continuous. On the other end, when both the bounds are set to integers, the variable becomes a discrete integer scalar. Note that minimizing on continuous variables is simpler so favor floats over integers when it makes sense.
