# Parameter sweeps
Hydra supports running jobs on Slurm or in a local queue using [fairtask](https://github.com/fairinternal/fairtask).

To use it, you need to drop in a hydra.yaml file into your config directory.

Among other things, hydra.yaml is configuring the fairtask launcher.
It also controls the job output directory when running normally or on the cluster, 
the logging configuration and more.

See the example [hydra.yaml](conf/hydra.yaml) in this demo.

sweep_example.py:
```python
@hydra.main(config_path='conf/config.yaml')
def experiment(cfg):
    log.info("Running on: {}".format(socket.gethostname()))
    print("Configuration:\n{}".format(cfg.pretty()))
```

We are back to using the logger, and we also print the hostname the code is running on.

Running parameter sweeps is easy, just add --sweep or -s.
The following command would run a single job with slurm, with all your default options:
```text
$ python demos/6_sweep/sweep_example.py --sweep
Sweep output dir : /checkpoint/omry/outputs/2019-06-27_01-41-00
Launching 1 jobs to slurm queue
        #0 :
Dask dashboard for "slurm" at http://localhost:8007.
```

Let's take a peak at the output:
```text
$ tree /checkpoint/omry/outputs/2019-06-27_01-41-00
/checkpoint/omry/outputs/2019-06-27_01-41-00
└── 0_14041239
    ├── config.yaml
    └── sweep_example.log
```

We have a config.yaml  file, which is dropped by hydra automatically, and also a sweep_example.log.
The hydra.yaml file is also configuring the logging properly.
In addition, there is a hidden .slurm sub directory that keeps stdout and stderr for each slurm job.

You can also sweep an arbitrary number of dimensions:
```text
$ python demos/4_sweep/sweep_example.py -s dataset=imagenet,cifar10 model=alexnet,resnet random_seed=0,1,3
Sweep output dir : /checkpoint/omry/outputs/2019-06-25_15-07-11/
Launching 12 jobs to slurm queue
        Workdir /checkpoint/omry/outputs/2019-06-25_15-07-11/0 : dataset=imagenet model=alexnet random_seed=0
        Workdir /checkpoint/omry/outputs/2019-06-25_15-07-11/1 : dataset=imagenet model=alexnet random_seed=1
        ...
        Workdir /checkpoint/omry/outputs/2019-06-25_15-07-11/10 : dataset=cifar10 model=resnet random_seed=1
        Workdir /checkpoint/omry/outputs/2019-06-25_15-07-11/11 : dataset=cifar10 model=resnet random_seed=3
Dask dashboard for "slurm" at http://localhost:8002.
```

In the example above, we combine sweeping on two datasets, two models and 3 random sees, for a total of 12 jobs.

Sweep support is currently very basic and this area will improve further.

[Prev](../5_defaults/README.md) [Up](../README.md) [Next](../7_objects/README.md)