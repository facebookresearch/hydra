# Parameter sweeps
Hydra supports running using fairtask.
To use it, you need to drop in a hydra.yaml file into your config directory.

Among other things, hydra.yaml is configuring the fairtask launcher.
It also controls the job output directory when running normally or on the cluster, 
the logging configuration and more.

See the example [hydra.yaml](conf/hydra.yaml) in this demo.

Running parameter sweeps is easy, just swap run with sweep as the first command:
```text
$ python demos/4_sweep/sweep_example.py --sweep
Sweep output dir : /checkpoint/omry/outputs/2019-06-25_13-49-01/
Launching 1 jobs to slurm queue
        Workdir /checkpoint/omry/outputs/2019-06-25_13-49-01/0 :
Dask dashboard for "slurm" at http://localhost:8001.
```
This runs a single job with the default config, but on slurm.

You can also sweep an arbitrary number of dimensions:
```text
$ python demos/4_sweep/sweep_example.py --sweep dataset=imagenet,cifar10 model=alexnet,resnet random_seed=0,1,3
Sweep output dir : /checkpoint/omry/outputs/2019-06-25_15-07-11/
Launching 12 jobs to slurm queue
        Workdir /checkpoint/omry/outputs/2019-06-25_15-07-11/0 : dataset=imagenet model=alexnet random_seed=0
        Workdir /checkpoint/omry/outputs/2019-06-25_15-07-11/1 : dataset=imagenet model=alexnet random_seed=1
        Workdir /checkpoint/omry/outputs/2019-06-25_15-07-11/2 : dataset=imagenet model=alexnet random_seed=3
        Workdir /checkpoint/omry/outputs/2019-06-25_15-07-11/3 : dataset=imagenet model=resnet random_seed=0
        Workdir /checkpoint/omry/outputs/2019-06-25_15-07-11/4 : dataset=imagenet model=resnet random_seed=1
        Workdir /checkpoint/omry/outputs/2019-06-25_15-07-11/5 : dataset=imagenet model=resnet random_seed=3
        Workdir /checkpoint/omry/outputs/2019-06-25_15-07-11/6 : dataset=cifar10 model=alexnet random_seed=0
        Workdir /checkpoint/omry/outputs/2019-06-25_15-07-11/7 : dataset=cifar10 model=alexnet random_seed=1
        Workdir /checkpoint/omry/outputs/2019-06-25_15-07-11/8 : dataset=cifar10 model=alexnet random_seed=3
        Workdir /checkpoint/omry/outputs/2019-06-25_15-07-11/9 : dataset=cifar10 model=resnet random_seed=0
        Workdir /checkpoint/omry/outputs/2019-06-25_15-07-11/10 : dataset=cifar10 model=resnet random_seed=1
        Workdir /checkpoint/omry/outputs/2019-06-25_15-07-11/11 : dataset=cifar10 model=resnet random_seed=3
Dask dashboard for "slurm" at http://localhost:8002.
```

In the example above, we combine sweeping on two datasets, two models and 3 random sees, for a total of 12 jobs.

Sweep support is currently very basic and this area will improve further.