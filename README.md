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


# Multi job runs
```
$ hydra sweep demos.obj_classify.Classify  model=alexnet,resnet optimizer=adam,nesterov something=one,two
Sweep output dir : /checkpoint/omry/outputs/2019-06-19_12-58-56/
Launching 8 jobs to slurm queue
        Workdir /checkpoint/omry/outputs/2019-06-19_12-58-56/0 : demos.obj_classify.Classify model=alexnet optimizer=adam something=one
        Workdir /checkpoint/omry/outputs/2019-06-19_12-58-56/1 : demos.obj_classify.Classify model=alexnet optimizer=adam something=two
        Workdir /checkpoint/omry/outputs/2019-06-19_12-58-56/2 : demos.obj_classify.Classify model=alexnet optimizer=nesterov something=one
        Workdir /checkpoint/omry/outputs/2019-06-19_12-58-56/3 : demos.obj_classify.Classify model=alexnet optimizer=nesterov something=two
        Workdir /checkpoint/omry/outputs/2019-06-19_12-58-56/4 : demos.obj_classify.Classify model=resnet optimizer=adam something=one
        Workdir /checkpoint/omry/outputs/2019-06-19_12-58-56/5 : demos.obj_classify.Classify model=resnet optimizer=adam something=two
        Workdir /checkpoint/omry/outputs/2019-06-19_12-58-56/6 : demos.obj_classify.Classify model=resnet optimizer=nesterov something=one
        Workdir /checkpoint/omry/outputs/2019-06-19_12-58-56/7 : demos.obj_classify.Classify model=resnet optimizer=nesterov something=two
```

# Debugging
## Running/debugging under pycharm
Run hydra as a module, and pass in your arguments. see screen shot. (TODO)

## Getting debug information about config composition:
If your configuration does not compose to what you want, you can use this command
to get information about what files were used to compose it and at what order.
```
hydra cfg demos.obj_classify.Classify optimizer=adam --debug
Loaded: /private/home/omry/dev/hydra/demos/obj_classify/conf/Classify.yaml
Loaded: /private/home/omry/dev/hydra/demos/obj_classify/conf/dataset/imagenet.yaml
Loaded: /private/home/omry/dev/hydra/demos/obj_classify/conf/model/alexnet.yaml
Loaded: /private/home/omry/dev/hydra/demos/obj_classify/conf/optimizer/adam.yaml
Not found: /private/home/omry/dev/hydra/demos/obj_classify/conf/optimizer/dataset/adam_imagenet.yaml
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