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
hydra run demos.obj_classify.Classify model=resent
```

Override model and optimizer
```
hydra run demos.obj_classify.Classify model=resent optimizer=adam optimizer.lr=0.001
```


# Multi job runs (typically to slurm) (TODO)

To run a job with 10 random seeds:
```
hydra multi demos.obj_classify.Classify model=resent
```


To run a the greed of (resnet,alexnet) X (nesterov,adam), which is 4 different experiments - each with 10 random seeds:
```
hydra multi demos.obj_classify.Classify -p model=resent,alexnet optimizer=nesterov,adam
```

# Debugging in pycharm
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