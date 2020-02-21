# Hydra Nevergrad Sweeper plugin example

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

#### Example of training using Nevergrad hyperparameter search
```text
$ python example/dummy_training.py -m db=mnist,cifar batch_size=4,8,16 lr='Log(a_min=0.001,a_max=1.0)' dropout=0.001:1.0
```

Example of the outputs of the last batch of 10 jobs (out of 100):
```
[2020-02-21 09:26:09,554][HYDRA] Launching 10 jobs locally
[2020-02-21 09:26:09,554][HYDRA] 	#0 : db=cifar batch_size=4 lr=0.03497970212569416 dropout=0.33002012968491873
[2020-02-21 09:26:09,712][root][INFO] - dummy_training(dropout=0.33002012968491873, lr=0.03497970212569416, db=cifar, batch_size=4) = 0.08504042755922456
[2020-02-21 09:26:09,713][HYDRA] 	#1 : db=cifar batch_size=4 lr=0.03590551571492024 dropout=0.33003635891401906
[2020-02-21 09:26:09,859][root][INFO] - dummy_training(dropout=0.33003635891401906, lr=0.03590551571492024, db=cifar, batch_size=4) = 0.0841308431990988
[2020-02-21 09:26:09,860][HYDRA] 	#2 : db=mnist batch_size=4 lr=0.03508269158529374 dropout=0.3301659686202661
[2020-02-21 09:26:10,003][root][INFO] - dummy_training(dropout=0.3301659686202661, lr=0.03508269158529374, db=mnist, batch_size=4) = 1.0850832770349725
[2020-02-21 09:26:10,004][HYDRA] 	#3 : db=cifar batch_size=4 lr=0.035222050729784946 dropout=0.3301621659635698
[2020-02-21 09:26:10,202][root][INFO] - dummy_training(dropout=0.3301621659635698, lr=0.035222050729784946, db=cifar, batch_size=4) = 0.08494011523378482
[2020-02-21 09:26:10,205][HYDRA] 	#4 : db=cifar batch_size=4 lr=0.03510125293118649 dropout=0.33282045448041886
[2020-02-21 09:26:10,356][root][INFO] - dummy_training(dropout=0.33282045448041886, lr=0.03510125293118649, db=cifar, batch_size=4) = 0.08771920154923235
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