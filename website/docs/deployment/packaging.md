---
id: app_packaging
title: Application packaging
sidebar_label: Application packaging 
---

You can package your Hydra app along with your configuration.
There is a working example [here](https://github.com/facebookresearch/hydra/tree/master/demos/hydra_app_example).

To install it, check-out the Hydra repo.
You can run it with:

```yaml
$ python demos/hydra_app_example/hydra_app/main.py
dataset:
  name: imagenet
  path: /datasets/imagenet
```

To install it, use:
```text
$ pip install demos/hydra_app_example/
Looking in indexes: https://pypi.org/simple, http://100.97.64.150
Processing ./demos/hydra_app_example
Building wheels for collected packages: hydra-app
  Building wheel for hydra-app (setup.py) ... done
  Created wheel for hydra-app: filename=hydra_app-0.1-cp36-none-any.whl size=2098 sha256=664e4acca715cb8a2c0041a56ee0a7bda44e5a562efe3d8fa7e9d210a12f9627
  Stored in directory: /tmp/pip-ephem-wheel-cache-e_e9v2k4/wheels/92/ed/23/2b589a6b3a31dbb1f01f224da50dcba825e6d597c2ec125690
Successfully built hydra-app
Installing collected packages: hydra-app
  Found existing installation: hydra-app 0.1
    Uninstalling hydra-app-0.1:
      Successfully uninstalled hydra-app-0.1
Successfully installed hydra-app-0.1
```

Once it's installed, you can run it with hydra_app:
```yaml
$ hydra_app
dataset:
  name: imagenet
  path: /datasets/imagenet
```

The installed app will use the packaged configuration files, and not the one from the checkout out repository.
