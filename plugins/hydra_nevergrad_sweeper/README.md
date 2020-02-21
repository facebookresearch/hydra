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
[2020-02-21 10:03:21,496][HYDRA] NevergradSweeper(optimizer=OnePlusOne, budget=100, num_workers=10) minimization
[2020-02-21 10:03:21,496][HYDRA] with parametrization Dict(batch_size=TransitionChoice(choices=Tuple(4,8,16),position=Scalar[recombination=average,sigma=Log{exp=1.2}[recombination=average,sigma=1.0]],transitions=[1. 1.]),db=Choice(choices=Tuple(mnist,cifar),weights=Array{(2,)}[recombination=average,sigma=1.0]),dropout=Scalar{Clipping(a_max=[1.], a_min=[0.], name=Cl([0.],[1.]), shape=(1,))}[recombination=average,sigma=Log{exp=1.2}[recombination=average,sigma=1.0]],lr=Log{exp=1.9952623149688797,Clipping(a_max=[1.], a_min=[0.001], name=Cl([0.001],[1.]), shape=(1,))}[recombination=average,sigma=1.0]):{'db': 'cifar', 'batch_size': 8, 'lr': 0.03162277660168379, 'dropout': 0.5}
[2020-02-21 10:03:21,498][HYDRA] Sweep output dir : multirun/2020-02-21/10-03-21
[2020-02-21 10:03:21,512][HYDRA] Launching 10 jobs locally
[2020-02-21 10:03:21,513][HYDRA]    #0 : db=mnist batch_size=8 lr=0.031622776601683784 dropout=0.5
[2020-02-21 10:03:21,617][root][INFO] - dummy_training(dropout=0.5, lr=0.031622776601683784, db=mnist, batch_size=8) = 5.258377223398316
[2020-02-21 10:03:21,620][HYDRA]    #1 : db=cifar batch_size=16 lr=0.03580028569948765 dropout=0.5733629848055519
[2020-02-21 10:03:21,720][root][INFO] - dummy_training(dropout=0.5733629848055519, lr=0.03580028569948765, db=cifar, batch_size=16) = 12.327562699106064
[2020-02-21 10:03:21,721][HYDRA]    #2 : db=cifar batch_size=16 lr=0.018086273752018992 dropout=0.4932938358052737
[2020-02-21 10:03:21,825][root][INFO] - dummy_training(dropout=0.4932938358052737, lr=0.018086273752018992, db=cifar, batch_size=16) = 12.265207562053254
[2020-02-21 10:03:21,826][HYDRA]    #3 : db=cifar batch_size=4 lr=0.030657177201676725 dropout=0.7677816541646862
[2020-02-21 10:03:21,934][root][INFO] - dummy_training(dropout=0.7677816541646862, lr=0.030657177201676725, db=cifar, batch_size=4) = 0.5271244769630095
[2020-02-21 10:03:21,935][HYDRA]    #4 : db=mnist batch_size=16 lr=0.021093062090794576 dropout=0.34188215594911286
[2020-02-21 10:03:22,049][root][INFO] - dummy_training(dropout=0.34188215594911286, lr=0.021093062090794576, db=mnist, batch_size=16) = 13.110789093858319
```


Example of the outputs of the last 5 evaluations (out of 100):
```text
[2020-02-21 09:26:10,357][HYDRA] 	#5 : db=mnist batch_size=4 lr=0.0346667594978735 dropout=0.32937253608049494
[2020-02-21 09:26:10,511][root][INFO] - dummy_training(dropout=0.32937253608049494, lr=0.0346667594978735, db=mnist, batch_size=4) = 1.0859607044216317
[2020-02-21 09:26:10,512][HYDRA] 	#6 : db=cifar batch_size=4 lr=0.035256650820510785 dropout=0.3300880416273387
[2020-02-21 09:26:10,662][root][INFO] - dummy_training(dropout=0.3300880416273387, lr=0.035256650820510785, db=cifar, batch_size=4) = 0.08483139080682787
[2020-02-21 09:26:10,664][HYDRA] 	#7 : db=cifar batch_size=4 lr=0.03551572322858361 dropout=0.32845315716844886
[2020-02-21 09:26:10,816][root][INFO] - dummy_training(dropout=0.32845315716844886, lr=0.03551572322858361, db=cifar, batch_size=4) = 0.08603111960296754
[2020-02-21 09:26:10,817][HYDRA] 	#8 : db=cifar batch_size=4 lr=0.035426085953820255 dropout=0.3299583448523775
[2020-02-21 09:26:10,963][root][INFO] - dummy_training(dropout=0.3299583448523775, lr=0.035426085953820255, db=cifar, batch_size=4) = 0.08461556919380224
[2020-02-21 09:26:10,964][HYDRA] 	#9 : db=cifar batch_size=4 lr=0.03496732134738235 dropout=0.3336075509908663
[2020-02-21 09:26:11,108][root][INFO] - dummy_training(dropout=0.3336075509908663, lr=0.03496732134738235, db=cifar, batch_size=4) = 0.08864022964348395
```
