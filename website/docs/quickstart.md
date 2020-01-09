---
id: quickstart
title: Quick start
---

## Installation

```
pip install hydra-core
```

## Basic example

Configuration file: `config.yaml`
```yaml
db:
  driver: mysql
  user: omry
  pass: secret
```

Python file: `my_app.py`
```python
import hydra
from omegaconf import DictConfig

@hydra.main(config_path="config.yaml")
def my_app(cfg : DictConfig) -> None:
    print(cfg.pretty())

if __name__ == "__main__":
    my_app()
```

You can learn more about OmegaConf [here](https://omegaconf.readthedocs.io/en/latest/usage.html#access-and-manipulation) later.

`config.yaml` is loaded automatically when you run your application
```yaml
$ python my_app.py
db:
  driver: mysql
  pass: secret
  user: omry
```

You can override values in the loaded config from the command line:
```yaml
$ python my_app.py db.user=root db.pass=1234
db:
  driver: mysql
  user: root
  pass: 1234
```

## Composition example
You may want to alternate between two different databases. to support this create a `config group` named db,
and place one config file for each alternative inside:
The directory structure of our application now looks like:
```text
├── conf
│   ├── config.yaml 
│   └── db
│       ├── mysql.yaml
│       └── postgresql.yaml
└── my_app.py
```

Here is the new `config.yaml`
```yaml
defaults:
    - db: mysql
```

`defaults` is a special directive telling Hydra to use db/mysql.yaml when composing the configuration object. 

You can now choose which database configuration to use from the and override values from the command line: 
```yaml
$ python my_app.py db=postgresql db.timeout=20
db:
  driver: postgresql
  pass: drowssap
  timeout: 20
  user: postgre_user
```
You can have as many config groups as you need.

## Multirun
You can run your function multiple times with different configuration easily with the `--multirun|-m` flag.


```
$ python my_app.py --multirun db=mysql,postgresql
[HYDRA] Sweep output dir : multirun/2020-01-09/01-16-29
[HYDRA] Launching 2 jobs locally
[HYDRA]        #0 : db=mysql
db:
  driver: mysql
  pass: secret
  user: omry

[HYDRA]        #1 : db=postgresql
db:
  driver: postgresql
  pass: drowssap
  timeout: 10
  user: postgre_user

```

There is a whole lot more to Hydra. Read the tutorial to learn more.