---
id: intro
title: Getting started
sidebar_label: Getting started
---

import useBaseUrl from '@docusaurus/useBaseUrl';
import Link from '@docusaurus/Link';

## Introduction
Hydra is an open-source Python framework that simplifies the development of research and other complex applications.
The key feature is the ability to dynamically create a hierarchical configuration by composition and override it through config files and the command line. 
The name Hydra comes from its ability to run multiple similar jobs - much like a Hydra with multiple heads.

### Key features:

* Hierarchical configuration composable from multiple sources
* Configuration can be specified or overridden from the command line
* Dynamic command line tab completion
* Run your application locally or launch it to run remotely
* Run multiple jobs with different arguments with a single command

## Versions

Hydra supports Linux, Mac and Windows.  
Use the version switcher in the top bar to switch between documentation versions.
 
|        |          Version          |  Release notes                                                                      | Python Versions    |
| -------|---------------------------|-------------------------------------------------------------------------------------| -------------------|
|        | 1.3 (Stable)              | [Release notes](https://github.com/facebookresearch/hydra/releases/tag/v1.3.0)      | **3.6 - 3.11**     |
| &#9658;| 1.2                       | [Release notes](https://github.com/facebookresearch/hydra/releases/tag/v1.2.0)      | **3.6 - 3.10**     |
|        | 1.1                       | [Release notes](https://github.com/facebookresearch/hydra/releases/tag/v1.1.1)      | **3.6 - 3.9**      |
|        | 1.0                       | [Release notes](https://github.com/facebookresearch/hydra/releases/tag/v1.0.7)      | **3.6 - 3.8**      |
|        | 0.11                      | [Release notes](https://github.com/facebookresearch/hydra/releases/tag/v0.11.3)     | **2.7, 3.5 - 3.8** |


## Quick start guide
This guide will show you some of the most important features you get by writing your application as a Hydra app.
If you only want to use Hydra for config composition, check out Hydra's [compose API](advanced/compose_api.md) for an alternative.
Please also read the full [tutorial](tutorials/basic/your_first_app/1_simple_cli.md) to gain a deeper understanding.

### Installation
```commandline
pip install hydra-core --upgrade
```

### Basic example
Config:
```yaml title="conf/config.yaml"
db:
  driver: mysql
  user: omry
  pass: secret
```
Application:
```python {4-6} title="my_app.py"
import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(cfg : DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

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
```yaml {4-5}
$ python my_app.py db.user=root db.pass=1234
db:
  driver: mysql
  user: root
  pass: 1234
```

### Composition example
You may want to alternate between two different databases. To support this create a `config group` named db,
and place one config file for each alternative inside:
The directory structure of our application now looks like:
```text
├── conf
│   ├── config.yaml
│   ├── db
│   │   ├── mysql.yaml
│   │   └── postgresql.yaml
│   └── __init__.py
└── my_app.py
```

Here is the new config:
```yaml title="conf/config.yaml"
defaults:
  - db: mysql
```

`defaults` is a special directive telling Hydra to use db/mysql.yaml when composing the configuration object.
The resulting cfg object is a composition of configs from defaults with configs specified in your `config.yaml`.

You can now choose which database configuration to use and override values from the command line: 
```yaml
$ python my_app.py db=postgresql db.timeout=20
db:
  driver: postgresql
  pass: drowssap
  timeout: 20
  user: postgres_user
```
You can have as many config groups as you need.

### Multirun
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
  user: postgres_user
```

There is a whole lot more to Hydra. Read the [tutorial](tutorials/basic/your_first_app/1_simple_cli.md) to learn more.

## Other stuff
### Community
Ask questions on github or StackOverflow (Use the tag #fb-hydra):
* [github](https://github.com/facebookresearch/hydra/discussions)
* [StackOverflow](https://stackoverflow.com/questions/tagged/fb-hydra)

Follow Hydra on Twitter and Facebook:
* [Facebook page](https://www.facebook.com/Hydra-Framework-109364473802509/)
* [Twitter](https://twitter.com/Hydra_Framework)


### Citing Hydra
If you use Hydra in your research please use the following BibTeX entry:
```text
@Misc{Yadan2019Hydra,
  author =       {Omry Yadan},
  title =        {Hydra - A framework for elegantly configuring complex applications},
  howpublished = {Github},
  year =         {2019},
  url =          {https://github.com/facebookresearch/hydra}
}
```
