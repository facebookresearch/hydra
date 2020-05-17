---
id: config_groups
title: Config groups
sidebar_label: Config groups
---
This is one of the most important concepts in Hydra.

Suppose you want to benchmark PostgreSQL and MySQL for your application.
When running of the application, you will need either MySQL or PostgreSQL - but not both.

The way to do this with Hydra is with a **Config group**.
A config group is a mutually exclusive set of configurations that are located together.

To create a config group, create a directory. e.g. `db` to hold a file for each database configuration alternative. 
Since we are expecting to have multiple config groups, we will proactively move all the configuration files 
into a `conf` directory.

Python file: `my_app.py`
```python
@hydra.main(config_path="conf")
def my_app(cfg: DictConfig) -> None:
    print(cfg.pretty())
```
`config_path` can specify the root directory for your configuration files relative to the declaring Python file.

``` text title="Directory layout"
├── conf
│   └── db
│       ├── mysql.yaml
│       └── postgresql.yaml
└── my_app.py
```

If you run my_app.py, it prints an empty config because no configuration was specified through `config_name`.
```yaml
$ python my_app.py
{}
```

You can now choose which database configuration to use from the command line:
```yaml
$ python my_app.py db=postgresql
db:
  driver: postgresql
  pass: drowssap
  timeout: 10
  user: postgre_user
```

Like before, you can still override individual values in the resulting config:
```yaml
$ python my_app.py db=postgresql db.timeout=20
db:
  driver: postgresql
  pass: drowssap
  timeout: 20
  user: postgre_user
```

This simple example demonstrated a very powerful feature of Hydra:
You can compose your configuration object from multiple configuration files.

For example, you can add a second config group controlling another aspect of your application:
```
$ python my_app.py db=postgresql walk=depth_first
```

TODO:

<div class="alert alert--info" role="alert">
The <b>@package</b> directive is new in Hydra 1.0.
This is an advanced topic and we will not cover it in this tutorial, You can learn more about 
it <a href="../../advanced/package_header">here</a>.<br/>
For now just put <b># @package: _group_</b> at the top of your config files.
</div><br/>
