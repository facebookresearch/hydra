---
id: getting_started
title: Getting started
sidebar_label: Getting started
---
The core Hydra framework supports Python 2.7 and modern Python 3.
Individual Hydra plugins may have stricter Python requirements.

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

## Developing
If you want to hack Hydra, you can install it in editable mode:

### Install:
Checkout this repository, Install Hydra and all the included plugins in development mode with:
```
pip install -e . && find ./plugins/ -name setup.py | xargs dirname | xargs pip install  -e 
```

### Uninstall 
Uninstall Hydra and all the included plugins with:
```
pip uninstall -y hydra && find ./plugins/ -name setup.py |\
xargs -i python {}  --name | xargs pip uninstall  -y
```
