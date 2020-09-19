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
 
|        |          Version          | Docs                          | Release notes                                                                                                       | Python Version   |
| -------|---------------------------|------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- | ---------------- |
| &#9658;| 1.0 (Stable)              | 1.0 Docs                                                                | [Release notes](https://github.com/facebookresearch/hydra/releases/tag/hydra-1.0.0rc1)  | **3.6+**         | 
|        | 0.11                      | <Link to={useBaseUrl("/docs/0.11/intro")}>**Switch to 0.11 Docs**</Link>| [Release notes](https://github.com/facebookresearch/hydra/releases/tag/0.11.0)          | 2.7, 3.5+        |


## Quick start guide
This guide will show you some of the most important features of Hydra.
Read the [tutorial](tutorials/basic/your_first_app/1_simple_cli.md) to gain a deeper understanding.

### Installation
```commandline
pip install hydra-core --upgrade
```

### Basic example
Config:
```yaml title="config.yaml"
db:
  driver: mysql
  user: omry
  pass: secret
```
Application:
```python {4-6} title="my_app.py"
import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(config_name="config")
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
├── db
│   ├── mysql.yaml
│   └── postgresql.yaml
├── config.yaml
└── my_app.py
```

Here is the new config:
```yaml title="config.yaml"
defaults:
  - db: mysql
```

`defaults` is a special directive telling Hydra to use db/mysql.yaml when composing the configuration object.
The resulting cfg object is a composition of configs from defaults with configs specified in your `config.yaml`.

You can now choose which database configuration to use from the and override values from the command line: 
```yaml
$ python my_app.py db=postgresql db.timeout=20
db:
  driver: postgresql
  pass: drowssap
  timeout: 20
  user: postgre_user
website:
  domain: example.com
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
website:
    domain: example.com

[HYDRA]        #1 : db=postgresql
db:
  driver: postgresql
  pass: drowssap
  timeout: 10
  user: postgre_user
website:
    domain: example.com
```

There is a whole lot more to Hydra. Read the [tutorial](tutorials/basic/your_first_app/1_simple_cli.md) to learn more.

## Other stuff
### Community
Ask questions in the chat or StackOverflow (Use the tag #fb-hydra):
* [Zulip Chat](https://hydra-framework.zulipchat.com)
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
