---
id: getting_started
title: Getting started
sidebar_label: Getting started
---
## Requirements
The core Hydra framework supports Python 2.7 and modern Python 3.
Specific plugins may have stricter Python requirements, for example both hydra-submitit and hydra-fairtask 
only support Python 3.6 or newer.

## Install/upgrade
A proper pip package will be available after Hydra is open sourced.
        
Install/upgrade Hydra and its plugins by running the following command:
```
pip install --upgrade --upgrade-strategy=eager \
'git+ssh://git@github.com/fairinternal/hydra.git@master' \
'git+ssh://git@github.com/fairinternal/hydra.git@master#subdirectory=plugins/fairtask' \
'git+ssh://git@github.com/fairinternal/hydra.git@master#subdirectory=plugins/submitit' 
```

## Uninstall
Uninstall Hydra and its plugins with:
```
pip uninstall hydra hydra-submitit hydra-fairtask -y
```
