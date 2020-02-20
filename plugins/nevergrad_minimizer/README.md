# Hydra example Launcher plugin

```yaml
defaults:
  - hydra/sweeper: nevergrad-minimizer
hydra:
  sweeper:
    params:
      budget: 4
      num_workers: 6
db: mnist
lr: 0.01
dropout: 0.6
batch_size: 4
```

#### Example of training using Nevergrad hyperparameter search
```text
$ python example/dummy_training.py -m db=mnist,cifar batch_size=4,8,16 lr='Log(a_min=0.001,a_max=1.0)' dropout=0.001:1.0
