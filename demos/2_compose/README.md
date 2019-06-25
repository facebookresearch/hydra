## Composing configuration
This example introduces the concept of composing configurations.
```bash
$ tree demos/2_compose/conf
demos/2_compose/conf
├── compose.py
├── dataset
│   ├── cifar10.yaml
│   └── imagenet.yaml
├── model
│   ├── alexnet.yaml
│   └── resnet.yaml
└── optimizer
    ├── adam.yaml
    └── nesterov.yaml
```

To tell hydra our config is in conf:
```python
@hydra.main(config_path='conf/')
def experiment(cfg):
    ...
```

We have 3 configuration families, a single run cab include a combination of dataset, model and optimizer.

If we just run compose nothing new is loaded:
```text
$ python demos/2_compose/compose.py
[2019-06-21 19:45:19,661][__main__][INFO] - Running on: devfair0260
[2019-06-21 19:45:19,662][__main__][INFO] - CWD: /private/home/omry/dev/hydra/outputs/2019-06-21_19-45-19
[2019-06-21 19:45:19,662][__main__][INFO] - Configuration:
{}
```

But we can tell Hydra to load the config for imagenet like this:
```text
$ python demos/2_compose/compose.py dataset=imagenet
[2019-06-21 19:46:20,296][__main__][INFO] - Running on: devfair0260
[2019-06-21 19:46:20,296][__main__][INFO] - CWD: /private/home/omry/dev/hydra/outputs/2019-06-21_19-46-20
[2019-06-21 19:46:20,296][__main__][INFO] - Configuration:
dataset:
  name: imagenet
  path: /datasets/imagenet
```

Or to load one of each family:
```text
$ python demos/2_compose/compose.py run dataset=imagenet optimizer=adam model=resnet
[2019-06-21 19:47:33,429][__main__][INFO] - Running on: devfair0260
[2019-06-21 19:47:33,429][__main__][INFO] - CWD: /private/home/omry/dev/hydra/outputs/2019-06-21_19-47-33
[2019-06-21 19:47:33,430][__main__][INFO] - Configuration:
dataset:
  name: imagenet
  path: /datasets/imagenet
model:
  num_layers: 50
  type: resnet
  width: 10
optimizer:
  beta: 0.01
  lr: 0.1
  type: adam
```

Repeating this every time you want to run can get annoying.
Time for the next demo.
