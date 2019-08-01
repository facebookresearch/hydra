---
id: example
title: Config groups
sidebar_label: Config groups
---
As you continue experimenting, you realize you want to try several different optimizers.
Let's add a second optimizer, `adam.yaml` and put both `nesterov.yaml` and `adam.yaml` in an optimizer subdirectory:
```text
$ tree 5_config_family/
examples/5_config_family/
├── README.md
├── conf
│   ├── config.yaml
│   └── optimizer
│       ├── adam.yaml
│       └── nesterov.yaml
└── experiment.py
```

### optimizer/adam.yaml
```yaml
optimizer:
  type: adam
  lr: 0.1
  beta: 0.01
```
### optimizer/nesterov.yaml
```yaml
optimizer:
  type: nesterov
  lr: 0.001
```

### config.yaml
To load `nesterov.yaml` we can do as we did before:
```yaml
defaults:
  - optimizer/nesterov
```
Running with this configuration, `nesterov.yaml` is loaded:
```yaml
$ python experiment.py
optimizer:
  lr: 0.001
  type: nesterov
```


But we can also do:
```yaml
defaults:
  - optimizer: nesterov
```

Very similar, but it allows us to do something quite nice:
```yaml
$ python experiment.py optimizer=adam
optimizer:
  beta: 0.01
  lr: 0.1
  type: adam
```

Woa, we loaded `optimizer/adam.yaml` instead of `optimizer/nesterov.yaml`!
We can still override individual values as before:
```yaml
$ python experiment.py optimizer=adam optimizer.beta=0.1
optimizer:
  beta: 0.1
  lr: 0.1
  type: adam
```
<div class="alert alert--info" role="alert">
<strong>NOTE</strong>: This example shows a single config group, but you can easily add as many as you want and load any combination 
of them at the same time.
</div>