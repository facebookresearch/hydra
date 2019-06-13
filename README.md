# Hydra
Hydra is a generic experimentation framework for scientific computing and machine learning

WIP


hydra init imageclassify

```
imageclassify/
    conf/
        imageclassify.yaml
        logging.yaml      
imageclassify/imageclassify.py
```

# Single job runs
hydra run mbrl -p env=cartpole dynamics_model=pe optimizer=random -o training.batch_size=32


# Multi job runs (typically to slurm)
hydra multi -p env=cartpole dynamics=pe -o training.batch_size=32
10 random seeds.

hydra multi -p env=cartpole dynamics_model=pe,de optimizer=random -o training.batch_size=32,64,128
==> 1 * 2 * 1 * 3 runs == 6 * 10 random seeds = 60 jobs.


# How to debug in pycharm
Run hydra as a module, and pass in your arguments. see screen shot. (TODO)

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