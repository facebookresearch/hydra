## Composing configuration
This demo introduces the concept of composing configurations.
We now have multipel configuration files, so let's put them in a conf subdirectory:

```bash
$ tree demos/2_compose/conf/
demos/2_compose/conf/
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

