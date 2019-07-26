---
id: getting_started
title: Getting started
sidebar_label: Getting started
---
## Requirements
The core Hydra framework supports Python 2.7 and modern Python 3.
Specific plugins may have stricter Pyton requirements, for example both hydra-submitit and hydra-fairtask 
only supports Python 3.6 or newer.

## Install/upgrade
A proper pip package will be available after Hydra is open sourced.

Install/upgrade Hydra and it's plugins by running the following command:
```
python3 -m pip install --upgrade --upgrade-strategy=eager \
'git+ssh://git@github.com/fairinternal/hydra.git@master' \
'git+ssh://git@github.com/fairinternal/hydra.git@master#subdirectory=plugins/fairtask' \
'git+ssh://git@github.com/fairinternal/hydra.git@master#subdirectory=plugins/submitit' 
```

## Uninstall
Uninstall Hydra and it's plugins with:
```
python3 -m pip uninstall hydra hydra-submitit hydra-fairtask -y
```
