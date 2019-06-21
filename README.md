# Hydra
Hydra is a generic experimentation framework for scientific computing and machine learning

# Installing
See developing for now.

# Basic usage
You can run the classify demo with the default arguments:

This is what the demo code looks like:
```python
import logging
import os
import sys

import socket

import hydra

log = logging.getLogger(__name__)

@hydra.main(config_path='conf/config.yaml')
def experiment(cfg):
    log.info("Running on: {}".format(socket.gethostname()))
    log.info("CWD: {}".format(os.path.realpath(os.getcwd())))
    log.info("Configuration:\n{}".format(cfg.pretty()))


if __name__ == "__main__":
    sys.exit(experiment())

```
It just prints a few things like the configuration object, the current working directory and the hostname.

```
$ python demos/classify/classify.py run
[2019-06-20 18:13:09,117][__main__][INFO] - Running on: devfair0260
[2019-06-20 18:13:09,117][__main__][INFO] - CWD: /private/home/omry/dev/hydra/outputs/2019-06-20_18-13-09
[2019-06-20 18:13:09,118][__main__][INFO] - Configuration:
dataset:
  name: imagenet
  path: /datasets/imagenet
model:
  num_layers: 7
  type: alexnet
optimizer:
  lr: 0.001
  type: nesterov
```

Note that working directory for the job changed to /private/home/omry/dev/hydra/outputs/2019-06-20_18-13-09. 
You should just write directly to the current working directory and not worry about where the output goes.
 
## Overriding individual values:
To change the value of the the learning rate:
```yaml
$ python demos/classify/classify.py run optimizer.lr=10
...
optimizer:
  lr: 10
  type: nesterov
```

## Composing configurations
under demos/classify/conf, we have subdirectories for dataset, model and optimizer.
```
$ tree demos/classify
demos/classify
├── classify.py
└── conf
    ├── config.yaml
    ├── hydra.yaml
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

* classify.py : entry point.
* conf/config.yaml : the main config file, typically this contains only details about default configurations to load etc
* dataset/{cifar10 , imagenet}.yaml : config snippets for the datasets imagenet and cifar10
* model/{alexnet, resnet}.yaml : config snippets for the models alexnet and resnet
* optimizers/{adam, nesterov}.yaml : config snippets for the optimizers adam and nesterov.

To change dataset:
```bash
$ python demos/classify/classify.py run dataset=cifar10
```
Results in the config:
```yaml
dataset:
  name: cifar10
  path: /datasets/cifar10
model:
  num_layers: 7
  type: alexnet
optimizer:
  lr: 0.001
  type: nesterov
```

To change dataset and optimizer:
```bash
$ python demos/classify/classify.py run dataset=cifar10 optimizer=adam
```
Resulting config:
```yaml
dataset:
  name: cifar10
  path: /datasets/cifar10
model:
  num_layers: 7
  type: alexnet
optimizer:
  beta: 0.01
  lr: 0.1
  type: adam
```

# Distributed runs and parameter sweeps
This will run two concurrent jobs on the cluster, one using alexnet as model and the second resnet.
```
$ python demos/classify/classify.py sweep model=alexnet,resnet
Sweep output dir : /checkpoint/omry/outputs/2019-06-20_19-14-02/
Launching 2 jobs to slurm queue
        Workdir /checkpoint/omry/outputs/2019-06-20_19-14-02/0 : model=alexnet
        Workdir /checkpoint/omry/outputs/2019-06-20_19-14-02/1 : model=resnet
```
You can sweep over multiple dimensions:
```
$ python demos/classify/classify.py sweep model=alexnet,resnet optimizer=adam,nesterov random_seed=1,2,3,4
Sweep output dir : /checkpoint/omry/outputs/2019-06-20_19-16-33/
Launching 16 jobs to slurm queue
        Workdir /checkpoint/omry/outputs/2019-06-20_19-16-33/0 : model=alexnet optimizer=adam random_seed=1
        Workdir /checkpoint/omry/outputs/2019-06-20_19-16-33/1 : model=alexnet optimizer=adam random_seed=2
        Workdir /checkpoint/omry/outputs/2019-06-20_19-16-33/2 : model=alexnet optimizer=adam random_seed=3
        Workdir /checkpoint/omry/outputs/2019-06-20_19-16-33/3 : model=alexnet optimizer=adam random_seed=4
        ...
```

## Getting debug information about config composition:
If your configuration does not compose to what you want, you can use this command
to get information about what files were used to compose it and at what order:
```
$ python demos/classify/classify.py cfg optimizer=adam  --debug
Loaded: /private/home/omry/dev/hydra/demos/classify/conf/config.yaml
Loaded: /private/home/omry/dev/hydra/demos/classify/conf/dataset/imagenet.yaml
Loaded: /private/home/omry/dev/hydra/demos/classify/conf/model/alexnet.yaml
Loaded: /private/home/omry/dev/hydra/demos/classify/conf/optimizer/adam.yaml
dataset:
...
```

# Developing
## Install:
```
python setup.py develop
```

## Uninstall
```
python setup.py develop --uninstall
rm $(which hydra)
```