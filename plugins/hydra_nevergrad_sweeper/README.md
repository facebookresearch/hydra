# Hydra Nevergrad Sweeper plugin

#### Example of training using Nevergrad hyperparameter search
```
Using the following configuration:
```yaml
defaults:
  - hydra/sweeper: nevergrad-sweeper
hydra:
  sweeper:
    params:
      budget: 100
      num_workers: 10
db: mnist
lr: 0.01
dropout: 0.6
batch_size: 4
```

And running with:
```text
$ python example/dummy_training.py -m db=mnist,cifar batch_size=4,8,16 lr='Log(a_min=0.001,a_max=1.0)' dropout=0.0:1.0
```

Example of the outputs for the initialization and the first 5 evaluations (out of 100):

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


Example of the outputs of the last 2 evaluations (out of 100):
```text
[HYDRA] 	#8 : db=mnist batch_size=4 lr=0.094 dropout=0.381
[__main__][INFO] - dummy_training(dropout=0.381, lr=0.094, db=mnist, batch_size=4) = 1.077
[HYDRA] 	#9 : db=mnist batch_size=4 lr=0.094 dropout=0.381
[__main__][INFO] - dummy_training(dropout=0.381, lr=0.094, db=mnist, batch_size=4) = 1.077
[HYDRA] Best parameters: db=mnist batch_size=4 lr=0.094 dropout=0.381
```


You will find an `optimization_results.yaml` file in your sweep folder with the parameters recommended by the optimizer:
```yaml
nevergrad:
  batch_size: 4
  db: mnist
  dropout: 0.381
  lr: 0.094
optimizer: nevergrad
```
