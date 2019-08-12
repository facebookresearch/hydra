---
id: getting_started
title: Getting started
sidebar_label: Getting started
---
### Requirements
The Hydra core supports Python 2.7 or Python 3.5 and later. 
Individual Hydra plugins may have stricter Python requirements.

### Install/upgrade
A proper pip package will be available after Hydra is open sourced.
For now, install/upgrade Hydra and its plugins by running the following command:
```
pip install --upgrade --upgrade-strategy=eager \
'git+ssh://git@github.com/facebookresearch/hydra.git@master' \
'git+ssh://git@github.com/facebookresearch/hydra.git@master#subdirectory=plugins/fairtask' \
'git+ssh://git@github.com/facebookresearch/hydra.git@master#subdirectory=plugins/submitit' 
```

### Uninstalling
```
pip uninstall -y hydra hydra-submitit hydra-fairtask
```


