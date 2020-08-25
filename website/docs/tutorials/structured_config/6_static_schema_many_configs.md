---
id: static_schema
title: Static schema with many configs
---
[![Example](https://img.shields.io/badge/-Example-informational)](https://github.com/facebookresearch/hydra/tree/master/examples/tutorials/structured_configs/6_static_schema_many_configs/)

We have seen that if the name of the config file matches the name of a configs stored in the `ConfigStore` it will be used to validate the config file automatically.
This is useful if there is a one-to-one mapping between the Structured Configs and the YAML files.
Such convenient mapping does not exist when we have many config files and just one schema.

If the config has a static structure, You can define it using Structured Configs. 
Any config merged into this config structure will be validated against the schema you define.

<div className="row">
<div className="col col--6">

```python
@dataclass
class DBConfig:
    driver: str = MISSING
    host: str = MISSING
    user: str = MISSING
    password: str = MISSING

@dataclass
class Config:
    db: DBConfig = MISSING

cs = ConfigStore.instance()
cs.store(name="config", node=Config)

@hydra.main(config_path="conf", 
            config_name="config")
def my_app(cfg: Config) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()



```

</div>

<div className="col  col--6">

```text title="Config directory"
├── config.yaml
└── db
    ├── prod.yaml
    ├── qa.yaml
    └── staging.yaml
``` 

```yaml title="config.yaml"
defaults:
  - db: staging
```

```yaml title="db/staging.yaml"
# @package _group_
driver: mysql
host: mysql001.staging
user: root
password: root
```

</div>
</div>

In the above example, the 3 yaml files has the structure compatible with the `Config` dataclass.
You can have as many such configs as you want.

```yaml title="Output"
$ python my_app.py db=prod
db:
  driver: mysql
  host: mysql001.prod
  user: root
  password: '1234'
```