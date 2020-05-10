---
id: defaults
title: Defaults
---

You can define a defaults list in your primary config just like you can in your primary config file.
The example below extends the previous example by adding a defaults list that will load db=mysql by default.

```python
@dataclass
class MySQLConfig:
    ...

@dataclass
class PostGreSQLConfig:
    ...

defaults = [
    # Load the config "mysql" from the config group "database"
    {"database": "mysql"}
]


@dataclass
class Config(DictConfig):
    # this is unfortunately verbose due to @dataclass limitations
    defaults: List[Any] = field(default_factory=lambda: defaults)
    db: MySQLConfig = MySQLConfig()



cs = ConfigStore.instance()
cs.store(group_path="database", name="mysql", path="db", node=MySQLConfig)
cs.store(group_path="database", name="postgresql", path="db", node=PostGreSQLConfig)
cs.store(name="config", node=Config)


@hydra.main(config_name="config")
def my_app(cfg: Config) -> None:
    print(cfg.pretty())


if __name__ == "__main__":
    my_app()
```
As expected, running it loads gives you the mysql config.
```yaml
$ python my_app.py
db:
  driver: mysql
  host: localhost
  password: secret
  port: 3306
  user: omry
```