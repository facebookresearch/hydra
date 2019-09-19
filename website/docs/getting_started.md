---
id: getting_started
title: Getting started
sidebar_label: Getting started
---
Hydra itself supports Python 2.7 and on Python >= 3.5.
Individual Hydra plugins may have stricter Python requirements, for example
hydra-fairtask and hydra-submitit requires Python 3.6 or newer.

### Install/upgrade
Install/upgrade Hydra:
```
pip install --upgrade hydra-core
```

### Using on the FAIR cluster
For use on the FAIR cluster, please additionally install the following plugins:
```
pip install --upgrade --upgrade-strategy=eager \
'git+ssh://git@github.com/facebookresearch/hydra.git@master#subdirectory=plugins/fairtask' \
'git+ssh://git@github.com/facebookresearch/hydra.git@master#subdirectory=plugins/submitit' \
'git+ssh://git@github.com/facebookresearch/hydra.git@master#subdirectory=plugins/fair_cluster'
```
