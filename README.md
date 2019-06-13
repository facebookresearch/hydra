# Hydra
Hydra is a generic experimentation framework for scientific computing and machine learning

# Installing
See developing for now.

# Single job runs
Run with all the default options
```
hydra run demos.obj_classify.Classify
```

Override model:
```
hydra run demos.obj_classify.Classify -p model=resent
```

Override model and optimizer
```
hydra run demos.obj_classify.Classify -p model=resent optimizer=adam
```


# Multi job runs (typically to slurm) (TODO)

hydra multi demos.obj_classify.Classify -p model=resent
10 random seeds.

hydra multi -p env=cartpole dynamics_model=pe,de optimizer=random -o training.batch_size=32,64,128
hydra multi demos.obj_classify.Classify -p model=resent,alexnet optimizer=nesterov,adam

will spawn 4 jobs, each one will run with 10 random seeds (40 jobs total)

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