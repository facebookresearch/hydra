[![CircleCI](https://circleci.com/gh/fairinternal/hydra.svg?style=svg&circle-token=af199cd2deca9e70e53776f9ded96284b10687e9)](https://circleci.com/gh/fairinternal/hydra)
# Hydra
Hydra is a experimentation framework providing the following:
 * A unified interface to run experiments locally or remotely
 * Dynamically composes a configuration from your own configuration primitives
 * Ability to override values in composed configurations from the command line
 * Creates a working directory per job run for you
 * Provides an ability to sweep on multiple dimensions from the command line
 * Configures python logger for your experiments

# Using
## Install
A proper pip package will be available after Hydra is open sourced.

You can install/upgrade by running the following command:
```
python3 -m pip install --upgrade --upgrade-strategy=eager \
'git+ssh://git@github.com/fairinternal/hydra.git@master' \
'git+ssh://git@github.com/fairinternal/hydra.git@master#subdirectory=plugins/hydra-fairtask' \
'git+ssh://git@github.com/fairinternal/hydra.git@master#subdirectory=plugins/hydra-submitit' 
```

## Uninstall
```
python3 -m pip uninstall hydra -y
```

# Basic usage
Go through the [demos](demos/README.md) to get a gentle incremental intruduction, starting from the most basic.


# Developing
## Install:
Checkout this repository, Install Hydra and all the included plugins in development mode with:
```
# install Hydra and plugins
pip install -e . && find ./plugins/ -name setup.py | xargs dirname | xargs pip install  -e 

```

## Uninstall 
Uninstall Hydra and all the included plugins with:
```
# Uninstall Hydra and plugins
pip uninstall -y hydra && find ./plugins/ -name setup.py | xargs -i python {}  --name | xargs pip uninstall  -y
```
