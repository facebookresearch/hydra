---
id: nevergrad_sweeper
title: Nevergrad Sweeper plugin
sidebar_label: Nevergrad Sweeper plugin
---

This plugin provides a mechanism for Hydra applications to use [Nevergrad](https://github.com/facebookresearch/nevergrad) algorithms for the optimization of experiments/applications parameters.

Install with:

```
pip install hydra_nevergrad_sweeper
```

Once installed, override `hydra/sweeper` in your config:

```yaml
defaults:
  - hydra/sweeper: nevergrad
```

#### Example of training using Nevergrad hyperparameter search

We include an example of how to use this plugin. The file [`example/dummy_training.py`](plugins/hydra_nevergrad_sweeper/example/dummy_training.py) implements an example of how to perform minimization of a (dummy) function including a mixture of continuous and discrete parameters. 


This application has the following configuration:
```yaml
defaults:
  - hydra/sweeper: nevergrad-sweeper

hydra:
  sweeper:
    params:
      # name of the nevergrad optimizer to use
      # OnePlusOne is good at low budget, but may converge early
      optimizer: OnePlusOne
      # total number of function evaluations to perform
      budget: 100
      # number of parallel workers for performing function evaluations
      num_workers: 10

db: mnist
lr: 0.01
dropout: 0.6
batch_size: 4
```

To compute the best parameters for this function, clone the code and run the following command in the `plugins/hydra_nevergrad_sweeper` directory:

```bash
python example/dummy_training.py -m db=mnist,cifar batch_size=4,8,16 lr='Log(a_min=0.001,a_max=1.0)' dropout=0.0:1.0
```

The output of a run looks like:
The initialization of the sweep and the first 5 evaluations (out of 100) look like this:

```text
[HYDRA] NevergradSweeper(optimizer=OnePlusOne, budget=100, num_workers=10) minimization
[HYDRA] with parametrization Dict(batch_size=TransitionChoice(choices=Tuple(4,8,16),position=Scalar[sigma=Log{exp=1.2}],transitions=[1. 1.]),db=Choice(choices=Tuple(mnist,cifar),weights=Array{(2,)}),dropout=Scalar{Cl(0,1)}[sigma=Log{exp=1.2}],lr=Log{exp=3.162277660168379,Cl(0.001,1)}):{'db': 'cifar', 'batch_size': 8, 'lr': 0.03162277660168379, 'dropout': 0.5}
[HYDRA] Sweep output dir: multirun/2020-03-04/17-53-29
[HYDRA] Launching 10 jobs locally
[HYDRA] 	#0 : db=mnist batch_size=8 lr=0.032 dropout=0.5
[__main__][INFO] - dummy_training(dropout=0.500, lr=0.032, db=mnist, batch_size=8) = 5.258
[HYDRA] 	#1 : db=mnist batch_size=16 lr=0.035 dropout=0.714
[__main__][INFO] - dummy_training(dropout=0.714, lr=0.035, db=mnist, batch_size=16) = 13.469
[HYDRA] 	#2 : db=cifar batch_size=8 lr=0.053 dropout=0.408
[__main__][INFO] - dummy_training(dropout=0.408, lr=0.053, db=cifar, batch_size=8) = 4.145
[HYDRA] 	#3 : db=cifar batch_size=8 lr=0.012 dropout=0.305
[__main__][INFO] - dummy_training(dropout=0.305, lr=0.012, db=cifar, batch_size=8) = 4.133
[HYDRA] 	#4 : db=mnist batch_size=4 lr=0.030 dropout=0.204
[__main__][INFO] - dummy_training(dropout=0.204, lr=0.030, db=mnist, batch_size=4) = 1.216
```


and the final 2 evaluations look like this:
```text
[HYDRA] 	#8 : db=mnist batch_size=4 lr=0.094 dropout=0.381
[__main__][INFO] - dummy_training(dropout=0.381, lr=0.094, db=mnist, batch_size=4) = 1.077
[HYDRA] 	#9 : db=mnist batch_size=4 lr=0.094 dropout=0.381
[__main__][INFO] - dummy_training(dropout=0.381, lr=0.094, db=mnist, batch_size=4) = 1.077
[HYDRA] Best parameters: db=mnist batch_size=4 lr=0.094 dropout=0.381
```


The run also creates an `optimization_results.yaml` file in your sweep folder with the parameters recommended by the optimizer:
```yaml
nevergrad:
  batch_size: 4
  db: mnist
  dropout: 0.381
  lr: 0.094

optimizer: nevergrad
```

#### Defining the parameters

In this example, we set the range of... TODO


#### About integers and floats

One important thing to note is how float and integers are interpreted in the command-line. When at least one of variable bounds is a float then the parameter is considered to be a float and be continuous. On the other end, when both the bounds are set to integers, the variable becomes a discrete integer scalar. Optimizing with continuous variables is easier so favor floats over integers when it makes sense.
