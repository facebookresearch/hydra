---
id: ray_launcher
title: Ray Launcher plugin
sidebar_label: Ray Launcher plugin
---
<!-- Add PyPI links etc -->

The Ray Launcher plugin provides 2 launchers: `ray_local` and `ray_aws`. `ray_local` will launch jobs on your local machine. `ray_aws` launches jobs remotely on AWS and is built on top of [Ray Autoscaler](https://docs.ray.io/en/latest/autoscaling.html).


This plugin requires Hydra 1.0 (Release candidate), to install:
```commandline
$ pip install hydra-ray-launcher --pre
```

After installation, override the Hydra launcher via your command line to activate one of the launchers:

```commandline
# Local Ray Launcher
$ python my_app.py hydra/launcher=ray_local
# AWS Ray Launcher
$ python my_app.py hydra/launcher=ray_aws
```

#### ray_local launcher

`ray_local` launcher starts `ray` by calling `ray.init()`on your local machines and wraps up your functions `my_func` in `@ray.remote` and then calls
`my_func.remote()` on them. You can easily config how your jobs are executed by changing `ray_local` launcher's configuration here <!-- Replace the path with link once it is available on hydra master --> 
 `~/hydra/plugins/hydra_ray_launcher/hydra_plugins/hydra_ray_launcher/conf/hydra/launcher/ray_local.yaml`
 
<!-- Add example link once it is available on hydra master -->
An example using the ray local launcher by default is provided in the plugin repository.

```commandline
$ pwd
<project_root>/hydra_ray_launcher/example/

$ python train.py -m
[2020-07-31 16:50:03,360][HYDRA] Ray Launcher is launching 1 jobs, sweep output dir: multirun/2020-07-31/16-50-02
[2020-07-31 16:50:03,360][HYDRA] Initializing ray with config: {'num_cpus': 2, 'num_gpus': 0}
2020-07-31 16:50:03,371 INFO resource_spec.py:204 -- Starting Ray with 8.64 GiB memory available for workers and up to 4.34 GiB for objects. You can adjust these settings with ray.init(memory=<bytes>, object_store_memory=<bytes>).
2020-07-31 16:50:03,749 INFO services.py:1168 -- View the Ray dashboard at localhost:8265
[2020-07-31 16:50:04,302][HYDRA]        #0 : random_seed=1
(pid=45515) [2020-07-31 16:50:04,614][__main__][INFO] - Start training...
(pid=45515) [2020-07-31 16:50:04,615][model.my_model][INFO] - Init my model
(pid=45515) [2020-07-31 16:50:04,615][model.my_model][INFO] - Created dir for checkpoints. dir=/Users/jieru/workspace/hydra-fork/hydra/plugins/hydra_ray_launcher/example/multirun/2020-07-31/16-50-02/0/checkpoint
```

Override `ray_init_cfg` to start ray with specific `ray.init()` config:
```commandline
$ python train.py hydra.launcher.params.ray_init_cfg.num_cpus=2 random_seed=1 -m
...
[HYDRA]Initializing ray with config: {'num_cpus': 2, 'num_gpus': 0}
...

```

 
#### ray_aws launcher

`ray_aws` launcher is built on top of ray's [autoscaler cli](https://docs.ray.io/en/latest/autoscaling.html). To get started, you need to 
config your AWS credentials first, tutorials can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).
Please make sure your AWS IAM user/role has `AmazonEC2FullAccess` and `IAMFullAccess` to avoid potential permission issues.
You can run an initial check on credential configuration running the following command.
```commandline
 python -c 'import boto3;boto3.client("ec2")'
```


`ray autoscaler` expects a yaml file to provide specs for the new cluster, which we've schematized in `hydra_ray_launcher.hydra_plugins.hydra_ray_launcher.conf.__init__.RayClusterConf`, 
The plugin defaults are in `conf/hydra/launcher/ray_aws.yaml`. You can override the default values in your app config or from command line.


<div class="alert alert--info" role="alert">
NOTE: To make sure plugin runs as expected, you need to make sure your local machine and your AWS cluster runs the same version of: `ray`, `hydra-core` and `python`. You can 
easily install the correct software version by overriding `RayClusterConf.setup_commands`
</div><br/>

Now we can go ahead and run `train.py` using `ray_aws` launcher

```commandline
$ tree -L 1
.
├── conf
├── model
└── train.py

$ python train.py hydra/launcher=ray_aws +ray_mode=aws random_seed=1,2,3 -m
...
[HYDRA] Ray Launcher is launching 3 jobs, 
[HYDRA]        #0 : ray_mode=aws random_seed=1
[HYDRA]        #1 : ray_mode=aws random_seed=2
[HYDRA]        #2 : ray_mode=aws random_seed=3
...
(pid=17975) [__main__][INFO] - Start training...
(pid=17975) [model.my_model][INFO] - Init my model.
(pid=17976) [__main__][INFO] - Start training...
(pid=17976) [model.my_model][INFO] - Init my model.
(pid=17976) [__main__][INFO] - Start training...
(pid=17976) [model.my_model][INFO] - Init my model. 
.....
[HYDRA] Stopped AWS cluster. since you've set your provider.cache_stopped_nodes to be True, we are not deleting the cluster.
```

In the example app config, we've configured the launcher to download ``*.pt`` files created by the app to local ``download`` dir. You should be able to see a ``download`` dir created in your current working dir.

```commandline
$ tree -L 1
.
├── conf
├── downloads # Created by example app train.py
├── model
├── multirun
└── train.py

$ tree downloads/
downloads/
└── multirun
    └── 2020-05-18
        └── 15-17-08
            ├── 0
            │   └── checkpoint
            │       └── checkpoint_1.pt
            ├── 1
            │   └── checkpoint
            │       └── checkpoint_2.pt
            └── 2
                └── checkpoint
                    └── checkpoint_3.pt
```


##### Manage Cluster LifeCycle
You can manage the Ray EC2 cluster lifecycle by configuring the two flags provided by the plugin:

- Default setting (no need to specify on commandline): Delete cluster after job finishes remotely:
```commandline
hydra.launcher.params.stop_cluster=True
hydra.launcher.params.ray_cluster_cfg.provider.cache_stopped_nodes=False
```

- Keep cluster running after jobs finishes remotely
```commandline
hydra.launcher.params.stop_cluster=False
```

- Power off EC2 instances without deletion
```commandline
hydra.launcher.params.ray_cluster_cfg.provider.cache_stopped_nodes=True
```

