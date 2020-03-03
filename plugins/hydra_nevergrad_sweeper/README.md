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
[HYDRA] with parametrization Dict(batch_size=TransitionChoice(choices=Tuple(4,8,16),position=Scalar[sigma=Log{exp=1.2}],transitions=[1. 1.]),db=Choice(choices=Tuple(mnist,cifar),weights=Array{(2,)}),dropout=Scalar{Cl([0.],[1.])}[sigma=Log{exp=1.2}],lr=Log{exp=1.9952623149688797,Cl([0.001],[1.])}):{'db': 'cifar', 'batch_size': 8, 'lr': 0.03162277660168379, 'dropout': 0.5}
[HYDRA] Sweep output dir : multirun/2020-02-21/10-03-21
[HYDRA] Launching 10 jobs locally
[HYDRA]    #0 : db=mnist batch_size=8 lr=0.031622776601683784 dropout=0.5
[__main__][INFO] - dummy_training(dropout=0.5, lr=0.031622776601683784, db=mnist, batch_size=8) = 5.258377223398316
[HYDRA]    #1 : db=cifar batch_size=16 lr=0.03580028569948765 dropout=0.5733629848055519
[__main__][INFO] - dummy_training(dropout=0.5733629848055519, lr=0.03580028569948765, db=cifar, batch_size=16) = 12.327562699106064
[HYDRA]    #2 : db=cifar batch_size=16 lr=0.018086273752018992 dropout=0.4932938358052737
[__main__][INFO] - dummy_training(dropout=0.4932938358052737, lr=0.018086273752018992, db=cifar, batch_size=16) = 12.265207562053254
[HYDRA]    #3 : db=cifar batch_size=4 lr=0.030657177201676725 dropout=0.7677816541646862
[__main__][INFO] - dummy_training(dropout=0.7677816541646862, lr=0.030657177201676725, db=cifar, batch_size=4) = 0.5271244769630095
[HYDRA]    #4 : db=mnist batch_size=16 lr=0.021093062090794576 dropout=0.34188215594911286
[__main__][INFO] - dummy_training(dropout=0.34188215594911286, lr=0.021093062090794576, db=mnist, batch_size=16) = 13.110789093858319
```


Example of the outputs of the last 5 evaluations (out of 100):
```text
[HYDRA] 	#5 : db=mnist batch_size=4 lr=0.0346667594978735 dropout=0.32937253608049494
[__main__][INFO] - dummy_training(dropout=0.32937253608049494, lr=0.0346667594978735, db=mnist, batch_size=4) = 1.0859607044216317
[HYDRA] 	#6 : db=cifar batch_size=4 lr=0.035256650820510785 dropout=0.3300880416273387
[__main__][INFO] - dummy_training(dropout=0.3300880416273387, lr=0.035256650820510785, db=cifar, batch_size=4) = 0.08483139080682787
[HYDRA] 	#7 : db=cifar batch_size=4 lr=0.03551572322858361 dropout=0.32845315716844886
[__main__][INFO] - dummy_training(dropout=0.32845315716844886, lr=0.03551572322858361, db=cifar, batch_size=4) = 0.08603111960296754
[HYDRA] 	#8 : db=cifar batch_size=4 lr=0.035426085953820255 dropout=0.3299583448523775
[__main__][INFO] - dummy_training(dropout=0.3299583448523775, lr=0.035426085953820255, db=cifar, batch_size=4) = 0.08461556919380224
[HYDRA] 	#9 : db=cifar batch_size=4 lr=0.03496732134738235 dropout=0.3336075509908663
[__main__][INFO] - dummy_training(dropout=0.3336075509908663, lr=0.03496732134738235, db=cifar, batch_size=4) = 0.08864022964348395
```


You will find an `optimization_results.yaml` file in your sweep folder with the parameters recommended by the optimizer:
```yaml
nevergrad:
  batch_size: 4
  db: mnist
  dropout: 0.34410367547736725
  lr: 0.11116748967967864
optimizer: nevergrad
```
