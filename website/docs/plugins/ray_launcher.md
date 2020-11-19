---
id: ray_launcher
title: Ray Launcher plugin
sidebar_label: Ray Launcher plugin
---

[![PyPI](https://img.shields.io/pypi/v/hydra-ray-launcher)](https://pypi.org/project/hydra-ray-launcher/)
![PyPI - License](https://img.shields.io/pypi/l/hydra-ray-launcher)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hydra-ray-launcher)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/hydra-ray-launcher.svg)](https://pypistats.org/packages/hydra-ray-launcher)
[![Example application](https://img.shields.io/badge/-Example%20application-informational)](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_ray_launcher/examples)
[![Plugin source](https://img.shields.io/badge/-Plugin%20source-informational)](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_ray_launcher)


The Ray Launcher plugin provides 2 launchers: `ray_aws` and `ray_local`. 
 `ray_aws` launches jobs remotely on AWS and is built on top of [Ray Autoscaler](https://docs.ray.io/en/latest/autoscaling.html). `ray_local` launches jobs on your local machine. 


### Installation

```commandline
$ pip install hydra-ray-launcher --pre
```

### Usage
Once installed, add `hydra/launcher=ray_aws` or `hydra/launcher=ray_local` to your command line. Alternatively, override `hydra/launcher` in your config:

```yaml
defaults:
  - hydra/launcher: ray_aws
```


### `ray_aws` launcher

:::important
`ray_aws` launcher is built on top of ray's [autoscaler cli](https://docs.ray.io/en/latest/autoscaling.html). To get started, you need to 
[config your AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).
`ray autoscaler` expects your AWS credentials have certain permissions for [`EC2`](https://aws.amazon.com/ec2) and [`IAM`](https://aws.amazon.com/iam). Read [this](https://github.com/ray-project/ray/issues/9327) for more information.
:::

`ray autoscaler` expects a yaml file to provide configuration for the EC2 cluster; we've schematized the configs in [`RayClusterConf`](https://github.com/facebookresearch/hydra/blob/master/plugins/hydra_ray_launcher/hydra_plugins/hydra_ray_launcher/conf/__init__.py), 

<details><summary>Discover ray_aws launcher's config</summary>

```commandline
$ python your_app.py hydra/launcher=ray_aws --cfg hydra -p hydra.launcher
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


#### Examples

<details><summary>Simple app</summary>

```commandline
$ python example/simple/my_app.py --multirun task=1,2,3
[HYDRA] Ray Launcher is launching 3 jobs, 
[HYDRA]        #0 : task=1
[HYDRA]        #1 : task=2
[HYDRA]        #2 : task=3
[HYDRA] Pickle for jobs: /var/folders/n_/9qzct77j68j6n9lh0lw3vjqcn96zxl/T/tmpqqg4v4i7/job_spec.pkl
[HYDRA] Saving RayClusterConf in a temp yaml file: /var/folders/n_/9qzct77j68j6n9lh0lw3vjqcn96zxl/T/tmpaa07pq3w.yaml.
...
[HYDRA] Output: INFO services.py:1164 -- View the Ray dashboard at http://127.0.0.1:8265
(pid=3374) [__main__][INFO] - Executing task 1
(pid=3374) [__main__][INFO] - Executing task 2
(pid=3374) [__main__][INFO] - Executing task 3
...
[HYDRA] Stopping cluster now. (stop_cluster=true)
[HYDRA] Deleted the cluster (provider.cache_stopped_nodes=false)
[HYDRA] Running command: ['ray', 'down', '-y', '/var/folders/n_/9qzct77j68j6n9lh0lw3vjqcn96zxl/T/tmpaa07pq3w.yaml']

```
</details>


<details><summary>Upload & Download from remote cluster</summary>

If your application is dependent on multiple modules, you can configure `hydra.launcher.sync_up` to upload dependency modules to the remote cluster.
You can also configure `hydra.launcher.sync_down` to download output from remote cluster if needed. This functionality is built on top of `rsync`, `include` and `exclude` is consistent with how it works in `rsync`.

```commandline

$  python train.py --multirun random_seed=1,2,3
[HYDRA] Ray Launcher is launching 3 jobs, 
[HYDRA]        #0 : random_seed=1
[HYDRA]        #1 : random_seed=2
[HYDRA]        #2 : random_seed=3
[HYDRA] Pickle for jobs: /var/folders/n_/9qzct77j68j6n9lh0lw3vjqcn96zxl/T/tmptdkye9of/job_spec.pkl
[HYDRA] Saving RayClusterConf in a temp yaml file: /var/folders/n_/9qzct77j68j6n9lh0lw3vjqcn96zxl/T/tmp2reaoixs.yaml.
[HYDRA] Running command: ['ray', 'up', '-y', '/var/folders/n_/9qzct77j68j6n9lh0lw3vjqcn96zxl/T/tmp2reaoixs.yaml']
...
[HYDRA] Output: INFO services.py:1164 -- View the Ray dashboard at http://127.0.0.1:8265
(pid=1772) [__main__][INFO] - Start training...
(pid=1772) [INFO] - Init my model
(pid=1772) [INFO] - Created dir for checkpoints. dir=checkpoint
(pid=1772) [__main__][INFO] - Start training...
(pid=1772) [INFO] - Init my model
(pid=1772) [INFO] - Created dir for checkpoints. dir=checkpoint
(pid=1772) [__main__][INFO] - Start training...
(pid=1772) [INFO] - Init my model
(pid=1772) [INFO] - Created dir for checkpoints. dir=checkpoint
Loaded cached provider configuration
...
[HYDRA] Output: receiving file list ... done
16-32-25/
16-32-25/0/
16-32-25/0/checkpoint/
16-32-25/0/checkpoint/checkpoint_1.pt
16-32-25/1/
16-32-25/1/checkpoint/
16-32-25/1/checkpoint/checkpoint_2.pt
16-32-25/2/
16-32-25/2/checkpoint/
16-32-25/2/checkpoint/checkpoint_3.pt
...
[HYDRA] Stopping cluster now. (stop_cluster=true)
[HYDRA] NOT deleting the cluster (provider.cache_stopped_nodes=true)
[HYDRA] Running command: ['ray', 'down', '-y', '/var/folders/n_/9qzct77j68j6n9lh0lw3vjqcn96zxl/T/tmpy430k4xr.yaml']
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


### `ray_local` launcher

`ray_local` launcher lets you run `ray` on your local machine. You can easily config how your jobs are executed by changing `ray_local` launcher's configuration here
 `~/hydra/plugins/hydra_ray_launcher/hydra_plugins/hydra_ray_launcher/conf/hydra/launcher/ray_local.yaml`
 
 The [example application](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_ray_launcher/examples/simple) starts a new ray cluster. 
```commandline
$ python my_app.py  --multirun hydra/launcher=ray_local
[HYDRA] Ray Launcher is launching 1 jobs, sweep output dir: multirun/2020-11-10/15-16-28
[HYDRA] Initializing ray with config: {}
INFO services.py:1164 -- View the Ray dashboard at http://127.0.0.1:8266
[HYDRA]        #0 : 
(pid=97801) [__main__][INFO] - Executing task 1
```

You can run the example application on your existing local ray cluster as well by overriding `hydra.launcher.ray_init_cfg.address`:
```commandline
$ python my_app.py  --multirun hydra/launcher=ray_local +hydra.launcher.ray_init_cfg='{address: localhost:6379}'
[HYDRA] Ray Launcher is launching 1 jobs, sweep output dir: multirun/2020-11-10/15-13-32
[HYDRA] Initializing ray with config: {'num_cpus': None, 'num_gpus': None, 'address': 'localhost:6379'}
INFO worker.py:633 -- Connecting to existing Ray cluster at address: 10.30.99.17:6379
[HYDRA]        #0 : 
(pid=93358) [__main__][INFO] - Executing task 1
```

### Configure `ray.init()` and `ray.remote()`
Ray launcher is built on top of [`ray.init()`](https://docs.ray.io/en/master/package-ref.html?highlight=ray.remote#ray-init) and [`ray.remote()`](https://docs.ray.io/en/master/package-ref.html?highlight=ray.remote#ray-remote). You can configure `ray` by overriding `hydra.launcher.ray_init_cfg` and `hydra.launcher.ray_remote_cfg`. Check out an [example config](https://github.com/facebookresearch/hydra/blob/master/plugins/hydra_ray_launcher/examples/simple/config.yaml).
