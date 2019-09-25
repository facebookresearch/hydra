---
id: config_groups
title: Config groups
sidebar_label: Config groups
---
This is the most important concept in Hydra.

After a while, you decide that it's time to add PostgreSQL support for your application.
When running of the application, you will need either MySQL or PostgreSQL - but not both.

The best way to represent this with Hydra is to create a directory - `db` - that will hold
a file for each database configuration alternative. 
We call this directory a config group.
To reduce clutter, we will also move `db` directory into `conf` - next to the Python file.
config_path specifies only the directory to find the configs.

Python file (`my_app.py`):
```python
@hydra.main(config_path="conf")
def my_app(cfg):
    print(cfg.pretty())
```

Note that in this example the `config_path` is a directory and not a config file like before.
This is the directory structure:
```text
├── conf
│   └── db
│       ├── mysql.yaml
│       └── postgresql.yaml
└── my_app.py
```

If you run it, it prints an empty config:
```yaml
$ python my_app.py
{}
```

But you can now choose which database snippet to merge into the `cfg` from the command line:
```yaml
$ python my_app.py db=mysql
db:
  driver: mysql
  pass: secret
  user: omry
```
Or:
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
You can compose your configuration object from multiple configuration snippets.
