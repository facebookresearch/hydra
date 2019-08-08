---
id: getting_started
title: Getting started
sidebar_label: Getting started
---
Hydra itself supports Python 2.7 and on Python >= 3.5.
Individual Hydra plugins may have stricter Python requirements, for example
hydra-fairtask and hydra-submitit requires Python 3.6 or newer.

### Install/upgrade
A proper pip package will be available after Hydra is open sourced.

Install/upgrade Hydra and its plugins by running the following command:
```
pip install --upgrade --upgrade-strategy=eager \
'git+ssh://git@github.com/facebookresearch/hydra.git@master' \
'git+ssh://git@github.com/facebookresearch/hydra.git@master#subdirectory=plugins/fairtask' \
'git+ssh://git@github.com/facebookresearch/hydra.git@master#subdirectory=plugins/submitit' 
```

### Uninstalling
pip uninstall -y hydra hydra-submitit hydra-fairtask


### Contributing
Check [this](https://github.com/facebookresearch/hydra/blob/master/CONTRIBUTING.md) If you want to be Hercules and hack Hydra.