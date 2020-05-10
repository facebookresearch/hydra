---
id: config_groups
title: Config groups
sidebar_label: Config groups
---
### Overview
This is one of the most important concepts in Hydra.

Suppose you want to benchmark PostgreSQL and MySQL for your application.
When running of the application, you will need either MySQL or PostgreSQL - but not both.

The way to do this with Hydra is with a **Config group**.
A config group is a mutually exclusive set of configuration files.

To create a config group, create a directory. e.g. `database` to hold a file for each database configuration alternative. 
Since we are expecting to have multiple config groups, we will proactively move all the configuration files 
into a `conf` directory.

```python title="Python file: my_app.py"
@hydra.main(config_path="conf")
def my_app(cfg: DictConfig) -> None:
    print(cfg.pretty())
```


`config_path` can specify your config file as in the [previous command line example](./1_simple_cli_app.md), or the root directory for your configuration files.
If a config file is specified, its directory is the root directory.

The directory structure of our application now looks like:
```text title="Directory structure"
├── conf
│   └── database
│       ├── mysql.yaml
│       └── postgresql.yaml
└── my_app.py
```

If you run my_app.py, it prints an empty config because no configuration was specified.
```yaml
$ python my_app.py
{}
```

You can now choose which database configuration to use from the command line:
```yaml
$ python my_app.py database=postgresql
db:
  driver: postgresql
  pass: drowssap
  timeout: 10
  user: postgre_user
```

Like before, you can still override individual values in the resulting config:
```yaml
$ python my_app.py database=postgresql db.timeout=20
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
$ python my_app.py database=postgresql walk=depth_first
```

### Naming your config groups
In the above example, we named the config group `database`.
```text title="Directory structure" {2}
├── conf
│   └── database
│       ├ ...
```

We have have the top-level config node `db`
```yaml title="Config file: config.yaml" {1}
db:
  driver: mysql
  ...
```
By convention, people usually use the same name for the config group and the top level config node. 
This page uses a different name to demonstrate that those two things are not linked.

You can follow the convention and use `db` for the config group:
```text title="Directory structure" {2}
├── conf
│   └── db
│       ├ ...
```

In this case, a perfectly valid command line override can look like:
```
$ python my_app.py db=postgresql db.timeout=20
```

Note how `db` has two meanings, the config group (`db=postgresql`), and the config node (`db.timeout=20`).

### Hierarchical config groups
For organizational purposes, you may use a hierarchy when you define your config groups.
If you are creating a library you expect others to use within their own applications, use a top level
directory for your config groups to avoid name collisions with groups provided by other user or by other libraries used by the user.

For example, Hydra itself has some configuration groups under the `hydra` sub directory.
``` text title="Directory structure"
└─── hydra
    ├── job_logging
    │   ├── default.yaml
    │   └── disabled.yaml
```

To override hierarchical configuration groups, use forward slash (`/`), for example:
```python
$ # Use 'default' job logging configuration:
$ python my_app.py hydra/job_logging=default
[2020-05-10 11:09:06,608][__main__][INFO] - Info level message

$ # Use 'disabled' job logging configuration:
$ python my_app.py hydra/job_logging=disabled
$ # no output
```
