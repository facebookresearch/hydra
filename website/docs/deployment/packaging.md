---
id: app_packaging
title: Application packaging
sidebar_label: Application packaging 
---

You can package your Hydra app along with your configuration.
There is a working example [here](https://github.com/facebookresearch/hydra/tree/master/tutorials/hydra_app_example).

To install it, check-out the Hydra repo.
You can run it with:

```yaml
$ python tutorial/hydra_app_example/hydra_app/main.py
dataset:
  name: imagenet
  path: /datasets/imagenet
```

To install it, use:
```text
$ pip install tutorial/hydra_app_example/
Processing ./tutorial/hydra_app_example
Building wheels for collected packages: hydra-app
  Building wheel for hydra-app (setup.py) ... done
  Created wheel for hydra-app: filename=hydra_app-0.1-cp36-none-any.whl size=2177 sha256=adce13a1b060021cd583c26883402e3cb99fd5967341e8ec955ff6b4dd683d78
  Stored in directory: /private/var/folders/sy/k0r_wfrj0z50jssb4hz_8pc80000gn/T/pip-ephem-wheel-cache-tne4nhow/wheels/09/22/37/ec791f52c97df23313d0131a9cdd3cd0db1814866f786e623a
Successfully built hydra-app
Installing collected packages: hydra-app
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
