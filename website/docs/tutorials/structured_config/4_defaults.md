---
id: defaults
title: Defaults
---

You can define a defaults list in your primary Structured Config just like you can in your primary `config.yaml` file.
The example below extends the previous example by adding a defaults list that will load `db=mysql` by default.

<div class="alert alert--info" role="alert">
NOTE: You can still place your defaults list in your primary (YAML) config file (Example in next page).
</div><br/>

```python
@dataclass
class MySQLConfig:
    ...

@dataclass
class PostGreSQLConfig:
    ...

defaults = [
    # Load the config "mysql" from the config group "db"
    {"db": "mysql"}
]

@dataclass
class Config(DictConfig):
    # this is unfortunately verbose due to @dataclass limitations
    defaults: List[Any] = field(default_factory=lambda: defaults)

    # Hydra will populate this field based on the defaults list
    db: Any = MISSING

cs = ConfigStore.instance()
cs.store(group="db", name="mysql", node=MySQLConfig)
cs.store(group="db", name="postgresql", node=PostGreSQLConfig)
cs.store(name="config", node=Config)


@hydra.main(config_name="config")
def my_app(cfg: Config) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
```
Running `my_app.py` loads the mysql config option by default:
```yaml
$ python my_app.py
db:
  driver: mysql
  ...
```

You can override the default option via the command line (note how we do not need `+` anymore, compared to the previous example):
```yaml
$ python my_app.py db=postgresql
db:
  driver: postgresql
  ...
```

Note also that the `db` command line argument can be made mandatory by using `MISSING` as default value:
```python
defaults = [
    # An error will be raised if the user forgets to specify `db=...`
    {"db": MISSING}
]
```
