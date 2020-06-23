---
id: jupyter_notebooks
title: Jupyter Notebooks
---

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/facebookresearch/hydra/master?filepath=examples%2jupyter_notebooks)
[![Notebook source](https://img.shields.io/badge/-Notebooks%20source-informational)](https://github.com/facebookresearch/hydra//tree/master/examples/jupyter_notebooks/)

### Notebooks
All the Notebooks share the configuration directory outlines below.  
The `__init__.py` file is needed is needed to help Python find the config files in some scenarios (It can be empty).  
```
conf/
├── application
│   ├── bananas.yaml
│   └── donkey.yaml
├── cloud_provider
│   ├── aws.yaml
│   └── local.yaml
├── db
│   ├── mysql.yaml
│   └── sqlite.yaml
├── environment
│   ├── production.yaml
│   └── testing.yaml
├── config.yaml
└── __init__.py      # __init__.py at the config top level directory is required
```

