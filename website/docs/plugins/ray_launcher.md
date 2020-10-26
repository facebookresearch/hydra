---
id: ray_launcher
title: Ray Launcher plugin
sidebar_label: Ray Launcher plugin
---
<!-- Add PyPI links etc -->

The Ray Launcher plugin provides 2 launchers: `ray_aws` and `ray_local`. `ray_aws` launches jobs remotely on AWS and is built on top of [Ray Autoscaler](https://docs.ray.io/en/latest/autoscaling.html). `ray_local` will launch jobs on your local machine. 


This plugin requires Hydra 1.0 to install:
```commandline
$ pip install hydra-ray-launcher --pre
```

After installation, override the Hydra launcher via your command line to activate one of the launchers:

```commandline
# AWS Ray Launcher
$ python my_app.py hydra/launcher=ray_aws

# Local Ray Launcher
$ python my_app.py hydra/launcher=ray_local
```

#### ray_aws launcher

`ray_aws` launcher is built on top of ray's [autoscaler cli](https://docs.ray.io/en/latest/autoscaling.html). To get started, you need to 
config your AWS credentials first, tutorials can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).
You can run an initial check on credential configuration running the following command.
```commandline
 python -c 'import boto3;boto3.client("ec2")'
```
:::caution
`ray autoscaler` expects your AWS user has certain permissions for `EC2` and `IAM`. This [issue](https://github.com/ray-project/ray/issues/9327) provides some contexts.
:::


`ray autoscaler` expects a yaml file to provide specs for the new cluster, which we've schematized in `hydra_ray_launcher.hydra_plugins.hydra_ray_launcher.conf.__init__.RayClusterConf`, 
The plugin defaults are in `conf/hydra/launcher/ray_aws.yaml`. You can override the default values in your app config or from command line.

:::caution
This plugins depends on `cloudpickle`, as a result please make sure your local machine and the AWS cluster runs the same version of: `ray`, `hydra-core` and `python`. You can install the desired software version by overriding `RayClusterConf.setup_commands`.
:::

Now we can go ahead and run `train.py` using `ray_aws` launcher

```commandline
$ tree -L 1
.
├── conf
├── model
└── train.py

$ python train.py --multirun hydra/launcher=ray_aws +extra_configs=aws random_seed=1,2,3 
...
[HYDRA] Ray Launcher is launching 3 jobs, 
[HYDRA]        #0 : +extra_configs=aws random_seed=1
[HYDRA]        #1 : +extra_configs=awsrandom_seed=2
[HYDRA]        #2 : +extra_configs=awsrandom_seed=3
...
(pid=17975) [__main__][INFO] - Start training...
(pid=17975) [model.my_model][INFO] - Init my model.
(pid=17976) [__main__][INFO] - Start training...
(pid=17976) [model.my_model][INFO] - Init my model.
(pid=17976) [__main__][INFO] - Start training...
(pid=17976) [model.my_model][INFO] - Init my model. 
.....
[HYDRA] Syncing outputs from remote dir: multirun/2020-08-05/11-41-04 to local dir: multirun/2020-08-05/11-41-04
...
[2020-10-14 15:18:20,888][HYDRA] Stopping cluster now. (stop_cluster=true)
[2020-10-14 15:18:20,889][HYDRA] NOT deleting the cluster (provider.cache_stopped_nodes=true)
```

In the example app config, we've configured the launcher to download ``*.pt`` files created by the app to local ``download`` dir. You should be able to see a ``download`` dir created in your current working dir.

<details><summary>Example app downloaded file</summary>
```commandline
$ tree -L 1
.
├── conf
├── multirun # Created by example app train.py
├── model
└── train.py

$ tree multirun/
multirun
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
</details>


<details><summary>Ray AWS Launcher config</summary>
You can discover the `ray_aws` launcher's config as follows:

```commandline
$ python train.py  hydra/launcher=ray_aws --cfg hydra -p hydra.launcher
# @package hydra.launcher
_target_: hydra_plugins.hydra_ray_launcher.ray_aws_launcher.RayAWSLauncher
mandatory_install:
  hydra_version: 1.0.3
  ray_version: 1.0.0
  cloudpickle_version: 1.6.0
  omegaconf_version: 2.1.0dev9
  pickle5_version: 0.0.11
  install_commands:
  - conda create -n hydra_${python_version:micro} python=${python_version:micro} -y
  - echo 'export PATH="$HOME/anaconda3/envs/hydra_${python_version:micro}/bin:$PATH"'
    >> ~/.bashrc
  - pip install omegaconf==${hydra.launcher.mandatory_install.omegaconf_version}
  - pip install hydra-core==${hydra.launcher.mandatory_install.hydra_version}
  - pip install ray==${hydra.launcher.mandatory_install.ray_version}
  - pip install cloudpickle==${hydra.launcher.mandatory_install.cloudpickle_version}
  - pip install pickle5==${hydra.launcher.mandatory_install.pickle5_version}
  - pip install -U https://hydra-test-us-west-2.s3-us-west-2.amazonaws.com/hydra_ray_launcher-0.1.0-py3-none-any.whl
ray_init_cfg:
  num_cpus: 1
  num_gpus: 0
ray_remote_cfg:
  num_cpus: 1
  num_gpus: 0
ray_cluster_cfg:
  cluster_name: default
  min_workers: 0
  max_workers: 1
  initial_workers: 0
  autoscaling_mode: default
  target_utilization_fraction: 0.8
  idle_timeout_minutes: 5
  docker:
    image: ''
    container_name: ''
    pull_before_run: true
    run_options: []
  provider:
    type: aws
    region: us-west-2
    availability_zone: us-west-2a,us-west-2b
    cache_stopped_nodes: false
    key_pair:
      key_name: hydra
  auth:
    ssh_user: ubuntu
  head_node:
    InstanceType: m5.large
    ImageId: ami-008d8ed4bd7dc2485
  worker_nodes:
    InstanceType: m5.large
    ImageId: ami-008d8ed4bd7dc2485
  file_mounts: {}
  initialization_commands: []
  setup_commands: []
  head_setup_commands: []
  worker_setup_commands: []
  head_start_ray_commands:
  - ray stop
  - ulimit -n 65536; ray start --head --redis-port=6379 --object-manager-port=8076
    --autoscaling-config=~/ray_bootstrap_config.yaml
  worker_start_ray_commands:
  - ray stop
  - ulimit -n 65536; ray start --address=$RAY_HEAD_IP:6379 --object-manager-port=8076
stop_cluster: true
sync_up:
  source_dir: null
  target_dir: null
  include: []
  exclude: []
sync_down:
  source_dir: null
  target_dir: null
  include: []
  exclude: []
```

</details>


##### Manage Cluster LifeCycle
You can manage the Ray EC2 cluster lifecycle by configuring the two flags provided by the plugin:

- Default setting (no need to specify on commandline): Delete cluster after job finishes remotely:
```commandline
hydra.launcher.stop_cluster=true
hydra.launcher.ray_cluster_cfg.provider.cache_stopped_nodes=False
```

- Keep cluster running after jobs finishes remotely
```commandline
hydra.launcher.stop_cluster=False
```

- Power off EC2 instances without deletion
```commandline
hydra.launcher.ray_cluster_cfg.provider.cache_stopped_nodes=true
```


#### ray_local launcher

`ray_local` launcher lets you run `ray` on your local machine. You can easily config how your jobs are executed by changing `ray_local` launcher's configuration here
 `~/hydra/plugins/hydra_ray_launcher/hydra_plugins/hydra_ray_launcher/conf/hydra/launcher/ray_local.yaml`
 
TODO Add example link once it is available on hydra master 
An example using the ray local launcher by default is provided in the plugin repository.

```commandline
$ python example/train.py --multirun
[2020-07-31 16:50:03,360][HYDRA] Ray Launcher is launching 1 jobs, sweep output dir: multirun/2020-07-31/16-50-02
[2020-07-31 16:50:03,360][HYDRA] Initializing ray with config: {'num_cpus': 2, 'num_gpus': 0}
2020-07-31 16:50:03,371 INFO resource_spec.py:204 -- Starting Ray with 8.64 GiB memory available for workers and up to 4.34 GiB for objects. You can adjust these settings with ray.init(memory=<bytes>, object_store_memory=<bytes>).
2020-07-31 16:50:03,749 INFO services.py:1168 -- View the Ray dashboard at localhost:8265
[2020-07-31 16:50:04,302][HYDRA]        #0 : random_seed=1
(pid=45515) [2020-07-31 16:50:04,614][__main__][INFO] - Start training...
(pid=45515) [2020-07-31 16:50:04,615][model.my_model][INFO] - Init my model
(pid=45515) [2020-07-31 16:50:04,615][model.my_model][INFO] - Created dir for checkpoints. dir=/Users/jieru/workspace/hydra-fork/hydra/plugins/hydra_ray_launcher/example/multirun/2020-07-31/16-50-02/0/checkpoint
```
You can discover the ray local launcher parameters with:

```yaml
$ python train.py --cfg hydra -p hydra.launcher
# @package hydra.launcher
target: hydra_plugins.hydra_ray_launcher.ray_local_launcher.RayLocalLauncher
params:
  ray_init_cfg:
    num_cpus: 1
    num_gpus: 0
  ray_remote_cfg:
    num_cpus: 1
    num_gpus: 0
```
