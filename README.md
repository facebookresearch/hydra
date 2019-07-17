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
git+ssh://git@github.com/fairinternal/hydra.git@master
```

## Uninstall
```
python3 -m pip uninstall hydra -y
```

# Basic usage
Go through the [demos](demos/README.md) to get a gentle incremental intruduction, starting from the most basic.


# Developing
## Install:
Checkout this repository, run the following and start hacking:
```
python setup.py develop
```

## Uninstall
```
python setup.py develop --uninstall
```
