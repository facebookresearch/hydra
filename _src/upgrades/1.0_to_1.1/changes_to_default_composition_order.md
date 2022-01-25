---
id: default_composition_order
title: Changes to default composition order
---
Default composition order is changing in Hydra 1.1.

For this example, let's assume the following two configs:
<div className="row">
<div className="col col--6">

```yaml title="config.yaml"
defaults:
  - foo: bar

foo:
  x: 10
```

</div>

<div className="col  col--6">

```yaml title="foo/bar.yaml"
# @package _group_
x: 20



```
</div>
</div>


<div className="row">
<div className="col">

In **Hydra 1.0**, configs from the Defaults List are overriding *config.yaml*, resulting in the following output:
</div>
<div className="col  col--4">

```yaml {2}
foo:
  x: 20
```
</div>
</div>



<div className="row">
<div className="col">

As of **Hydra 1.1**, *config.yaml* is overriding configs from the Defaults List, resulting in the following output:
</div>
<div className="col  col--4">

```yaml {2}
foo:
  x: 10
```
</div>
</div>



## Migration
If your application uses `hydra.main`, the best way to verify that updating Hydra versions does not change your job configurations is to compare the output of `python my_app.py --cfg job` on both the new and old Hydra versions. If your application uses the Compose API, please make sure you have comprehensive unit tests on the composed configuration.

### Primary config is a YAML file
To ensure this change is not missed by people migrating from Hydra 1.0, Hydra 1.1 issues a warning if the Defaults List in the primary config is missing `_self_`, and there are config values in addition to the Defaults List.  
To address the warning, add `_self_` to the Defaults List of the primary config.

- If the new behavior works for your application, append `_self_` to the end of the Defaults List.
- If your application requires the previous behavior, insert `_self_` as the first item in your Defaults List.


<div className="row">
<div className="col col--6">

```yaml title="config.yaml" {2}
defaults:
  - _self_
  - foo: bar

foo:
  x: 10
```
</div>

<div className="col  col--6">

```yaml title="Output config"
foo:
  x: 20




```
</div>
</div>


The Defaults List is described [here](/advanced/defaults_list.md).

### Primary config is a Structured Config
Structured Configs used as primary config may see changes as well.
You should add `_self_` to the defaults list to indicate the composition order. In such cases you will typically want `_self_` to be the first item in the defaults list. 

```python {3,14}
defaults = [
    "_self_",
    {"db": "mysql"}
]

@dataclass
class Config:
    # this is unfortunately verbose due to @dataclass limitations
    defaults: List[Any] = field(default_factory=lambda: defaults)

    # Hydra will populate this field based on the defaults list
    db: Any = MISSING
```

### Primary config is a config file with a Structured Config schema
If you use Structured Config as a schema for your primary config, be sure to add `_self_` after the schema in the Defaults List, otherwise the schema will override the config instead of the other way around.

<div className="row">
<div className="col col--4">

```python title="my_app.py"
@dataclass
class Config:
  host: str = "localhost"
  port: int = 8080

cs.store(name="base_config", 
         node=Config)
```

</div>

<div className="col  col--4">

```yaml {3,5} title="config.yaml"
defaults:
 - base_config  # schema
 - _self_       # after schema

port: 3306


```

</div>

<div className="col  col--4">

```yaml {2} title="Output config"
host: localhost # schema
port: 3306      # config.yaml





```

</div>

</div>


### Compatibility with both Hydra 1.0 and 1.1
If your config must be compatible with both Hydra 1.0 and 1.1, Insert `_self_` as the first item in the Defaults List.
Hydra 1.0.7 (or newer releases in Hydra 1.0) ignores `_self_` in the Defaults List and Hydra 1.1 will compose the same config as Hydra 1.0 if `_self_` is the first item.
