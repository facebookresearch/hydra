## Jupyter notebooks
There are multiple Jupyter notebooks here.
You can run them via [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/facebookresearch/hydra/master?filepath=examples%2jupyter_notebooks)

All the notebooks share the same configuration directory, described below.  
The `__init__.py` file is needed is needed to help Python find the config files in some scenarios (It can be empty).  
It is recommended that you always place such a file on your config directory.  
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

