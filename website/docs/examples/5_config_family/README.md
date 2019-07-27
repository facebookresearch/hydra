---
id: example
title: Config family
sidebar_label: Config family
---
As you continue experimenting, you realize want to try several different optimizers.
Let's add a second optimizer, adam.yaml and put both nesterov and adam in an optimizer subdirectory:
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
Here is the content of adam.yaml:
```yaml
optimizer:
  type: adam
  lr: 0.1
  beta: 0.01
```
### optimizer/nesterov.yaml
Here is the content of nesterov.yaml:
```yaml
optimizer:
  type: nesterov
  lr: 0.001
```

### config.yaml
One alternative to load one of the two is do what we did before:
```yaml
defaults:
  - optimizer/nesterov
```
Running with this configuration, nesterov is loaded:
```yaml
python experiment.py
optimizer:
  lr: 0.001
  type: nesterov
```

But we can also do:
```yaml
defaults:
  - optimizer: nesterov
```

Very similar, but it allow us to do something quiet nice:
```yaml
$ python experiment.py optimizer=adam
optimizer:
  beta: 0.01
  lr: 0.1
  type: adam
```

Woa, we loaded optimizer/adam.yaml instead of optimizer/nesterov.yaml!
We can still override individual values as before:
```yaml
$ python experiment.py optimizer=adam optimizer.beta=0.1
optimizer:
  beta: 0.1
  lr: 0.1
  type: adam
```
