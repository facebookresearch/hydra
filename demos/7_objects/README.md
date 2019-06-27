## Objects
A common pattern is to instantiate different types of objects based on the configuration, potentially passing different arguments to object.
For example, we may have a hierarchy of models, where two different classes implement the same model interface,
but taking different arguments in the initialization.

```python
class Model:
    def __init__(self):
        pass

    def forward(self, x):
        pass


class Alexnet(Model):
    def __init__(self, num_layers):
        log.info(f"Alexnet : num_layers={num_layers}")
        self.num_layers = num_layers

    def forward(self, x):
        log.info(f"Alexnet forward({x})")


class Resnet(Model):
    def __init__(self, num_layers, width):
        log.info(f"Resnet : num_layers={num_layers}, width={width}")
        self.num_layers = num_layers
        self.width = width

    def forward(self, x):
        log.info(f"Resnet : forward({x})")
```

To support this, we can have a parallel config structure:
```text
demos/5_objects/conf/
├── config.yaml
└── model
    ├── alexnet.yaml
    └── resnet.yaml
```

model/alexnet.yaml:
```yaml
model:
  class: demos.5_objects.objects.Alexnet
  params:
    num_layers: 7
```
model/resenet.yaml:
```yaml
model:
  class: demos.5_objects.objects.Resnet
  params:
    num_layers: 50
    width: 10
```

Finally, out code instantiate the object from the configuraiton in just 1 line of code:
```python
@hydra.main(config_path='conf/config.yaml')
def objects(cfg):
    print(cfg.pretty())
    model = hydra.utils.instantiate(cfg.model)
    model.forward(10)
```

As before, you can override parameters in the config:
```yaml
$ python demos/7_objects/objects.py
model:
  class: demos.7_objects.objects.Alexnet
  params:
    num_layers: 7

Alexnet: num_layers=7
Alexnet: forward(10)
```

Or combine composition and overriding:
```yaml
$ python demos/7_objects/objects.py  model=resnet model.params.num_layers=100
model:
  class: demos.7_objects.objects.Resnet
  params:
    num_layers: 100
    width: 10

Resnet: num_layers=100, width=10
Resnet: forward(10)
```

[[Prev](../6_sweep/README.md)] [[Up](../README.md)]