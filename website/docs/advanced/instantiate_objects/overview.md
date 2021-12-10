---
id: overview
title: Instantiating objects with Hydra
sidebar_label: Overview
---

import {ExampleGithubLink} from "@site/src/components/GithubLink"

<ExampleGithubLink text="Example applications" to="examples/instantiate"/>

One of the best ways to drive different behavior in an application is to instantiate different implementations of an interface.
The code using the instantiated object only knows the interface which remains constant, but the behavior
is determined by the actual object instance.

Hydra provides `hydra.utils.instantiate()` (and its alias `hydra.utils.call()`) for instantiating objects and calling functions. Prefer `instantiate` for creating objects and `call` for invoking functions.

Call/instantiate supports:
- Constructing an object by calling the `__init__` method
- Calling functions, static functions, class methods and other callable global objects

<details><summary>Instantiate API (Expand for details)</summary>

```python
def instantiate(config: Any, *args: Any, **kwargs: Any) -> Any:
    """
    :param config: An config object describing what to call and what params to use.
                   In addition to the parameters, the config must contain:
                   _target_ : target class or callable name (str)
                   And may contain:
                   _args_: List-like of positional arguments to pass to the target
                   _recursive_: Construct nested objects as well (bool).
                                True by default.
                                may be overridden via a _recursive_ key in
                                the kwargs
                   _convert_: Conversion strategy
                        none    : Passed objects are DictConfig and ListConfig, default
                        partial : Passed objects are converted to dict and list, with
                                  the exception of Structured Configs (and their fields).
                        all     : Passed objects are dicts, lists and primitives without
                                  a trace of OmegaConf containers
                   _partial_: If True, return functools.partial wrapped method or object
                              False by default. Configure per target.
    :param args: Optional positional parameters pass-through
    :param kwargs: Optional named parameters to override
                   parameters in the config object. Parameters not present
                   in the config objects are being passed as is to the target.
                   IMPORTANT: dataclasses instances in kwargs are interpreted as config
                              and cannot be used as passthrough
    :return: if _target_ is a class name: the instantiated object
             if _target_ is a callable: the return value of the call
    """

# Alias for instantiate
call = instantiate
```

</details><br/>

The config passed to these functions must have a key called `_target_`, with the value of a fully qualified class name, class method, static method or callable.
For convenience, `None` config results in a `None` object.

**Named arguments** : Config fields (except reserved fields like `_target_`) are passed as named arguments to the target.
Named arguments in the config can be overridden by passing named argument with the same name in the `instantiate()` call-site.

**Positional arguments** : The config may contain a `_args_` field representing positional arguments to pass to the target.
The positional arguments can be overridden together by passing positional arguments in the `instantiate()` call-site.



### Simple usage
Your application might have an Optimizer class:
```python title="Example class"
class Optimizer:
    algo: str
    lr: float

    def __init__(self, algo: str, lr: float) -> None:
        self.algo = algo
        self.lr = lr
```

<div className="row">

<div className="col col--6">

```yaml title="Config"
optimizer:
  _target_: my_app.Optimizer
  algo: SGD
  lr: 0.01




```


</div>

<div className="col col--6">

```python title="Instantiation"
opt = instantiate(cfg.optimizer)
print(opt)
# Optimizer(algo=SGD,lr=0.01)

# override parameters on the call-site
opt = instantiate(cfg.optimizer, lr=0.2)
print(opt)
# Optimizer(algo=SGD,lr=0.2)
```

</div>
</div>


### Recursive instantiation
Let's add a Dataset and a Trainer class. The trainer holds a Dataset and an Optimizer instances.
```python title="Additional classes"
class Dataset:
    name: str
    path: str

    def __init__(self, name: str, path: str) -> None:
        self.name = name
        self.path = path


class Trainer:
    def __init__(self, optimizer: Optimizer, dataset: Dataset) -> None:
        self.optimizer = optimizer
        self.dataset = dataset
```

With the following config, you can instantiate the whole thing with a single call:
```yaml title="Example config"
trainer:
  _target_: my_app.Trainer
  optimizer:
    _target_: my_app.Optimizer
    algo: SGD
    lr: 0.01
  dataset:
    _target_: my_app.Dataset
    name: Imagenet
    path: /datasets/imagenet
```

Hydra will instantiate nested objects recursively by default.
```python
trainer = instantiate(cfg.trainer)
print(trainer)
# Trainer(
#  optimizer=Optimizer(algo=SGD,lr=0.01),
#  dataset=Dataset(name=Imagenet, path=/datasets/imagenet)
# )
```
You can override parameters for nested objects:
```python
trainer = instantiate(
    cfg.trainer,
    optimizer={"lr": 0.3},
    dataset={"name": "cifar10", "path": "/datasets/cifar10"},
)
print(trainer)
# Trainer(
#   optimizer=Optimizer(algo=SGD,lr=0.3),
#   dataset=Dataset(name=cifar10, path=/datasets/cifar10)
# )
```

Similarly, positional arguments of nested objects can be overridden:
```python
obj = instantiate(
    cfg.object,
    # pass 1 and 2 as positional arguments to the target object
    1, 2,  
    # pass 3 and 4 as positional arguments to a nested child object
    child={"_args_": [3, 4]},
)
```

### Disable recursive instantiation
You can disable recursive instantiation by setting `_recursive_` to `False` in the config node or in the call-site
In that case the Trainer object will receive an OmegaConf DictConfig for nested dataset and optimizer instead of the instantiated objects.
```python
optimizer = instantiate(cfg.trainer, _recursive_=False)
print(optimizer)
```

Output:
```python
Trainer(
  optimizer={
    '_target_': 'my_app.Optimizer', 'algo': 'SGD', 'lr': 0.01
  },
  dataset={
    '_target_': 'my_app.Dataset', 'name': 'Imagenet', 'path': '/datasets/imagenet'
  }
)
```

### Parameter conversion strategies
By default, the parameters passed to the target are either primitives (int, float, bool etc) or                                                                                                 
OmegaConf containers (DictConfig, ListConfig).
OmegaConf containers have many advantages over primitive dicts and lists but in some cases 
it's desired to pass a real dicts and lists (for example, for performance reasons).

You can change the parameter conversion strategy using the `_convert_` parameter (in your config or the call-site).
Supported values are:

- `none` : Default behavior, Use OmegaConf containers
- `partial` : Convert OmegaConf containers to dict and list, except Structured Configs.
- `all` : Convert everything to primitive containers

Note that the conversion strategy applies to all the parameters passed to the target.

### Partial Instantiation
Sometimes you may not set all parameters needed to instantiate an object from the configuration, in this case you can set
`_partial_` to be `True` to get a `functools.partial` wrapped object or method, then complete initializing the object in 
the application code. Here is an example:

```python title="Example classes"
class Optimizer:
    algo: str
    lr: float

    def __init__(self, algo: str, lr: float) -> None:
        self.algo = algo
        self.lr = lr

    def __repr__(self) -> str:
        return f"Optimizer(algo={self.algo},lr={self.lr})"


class Model:
    def __init__(self, optim_partial: Any, lr: float):
        super().__init__()
        self.optim = optim_partial(lr=lr)
        self.lr = lr

    def __repr__(self) -> str:
        return f"Model(Optimizer={self.optim},lr={self.lr})"
```

<div className="row">

<div className="col col--5">

```yaml title="Config"
model:
  _target_: my_app.Model
  optim_partial:
    _partial_: true
    _target_: my_app.Optimizer
    algo: SGD
  lr: 0.01
```


</div>

<div className="col col--7">

```python title="Instantiation"
model = instantiate(cfg.model)
print(model)
# "Model(Optimizer=Optimizer(algo=SGD,lr=0.01),lr=0.01)




```

</div>
</div>
