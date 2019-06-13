# Hydra
Hydra is a generic experimentation framework for scientific computing and machine learning

# Installing
See developing for now.

# Single job runs
The demo project can be anywhere in your file system as long as you have hydra installed.
```
hydra run demo_project.discombobulator.Task1 -p env=cartpole -o training.batch_size=32
hydra run demo_project.discombobulator.Task1 -p env=cartpole dynamics=pe 
```

# Multi job runs (typically to slurm) (TODO)
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