[![CircleCI](https://circleci.com/gh/fairinternal/hydra.svg?style=svg&circle-token=af199cd2deca9e70e53776f9ded96284b10687e9)](https://circleci.com/gh/fairinternal/hydra)
# Hydra
Hydra is an experimentation framework.

Its mission is to make experimentation great again.

The the [web site](https://fairinternal.github.io/hydra/) for more information.


## Developing
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
