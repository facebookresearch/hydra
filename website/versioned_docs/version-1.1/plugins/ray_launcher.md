---
id: ray_launcher
title: Ray Launcher plugin
sidebar_label: Ray Launcher plugin
---

import GithubLink,{ExampleGithubLink} from "@site/src/components/GithubLink"

[![PyPI](https://img.shields.io/pypi/v/hydra-ray-launcher)](https://pypi.org/project/hydra-ray-launcher/)
![PyPI - License](https://img.shields.io/pypi/l/hydra-ray-launcher)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hydra-ray-launcher)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/hydra-ray-launcher.svg)](https://pypistats.org/packages/hydra-ray-launcher)<ExampleGithubLink text="Example application" to="plugins/hydra_ray_launcher/examples"/><ExampleGithubLink text="Plugin source" to="plugins/hydra_ray_launcher"/>

The Ray Launcher plugin provides 2 launchers: `ray_aws` and `ray`.
 `ray_aws` launches jobs remotely on AWS and is built on top of [ray autoscaler sdk](https://docs.ray.io/en/releases-1.3.0/cluster/sdk.html). `ray` launches jobs on your local machine or existing ray cluster.

### Installation

```commandline
$ pip install hydra-ray-launcher --upgrade
```

### Usage
Once installed, add `hydra/launcher=ray_aws` or `hydra/launcher=ray` to your command line. Alternatively, override `hydra/launcher` in your config:

```yaml
defaults:
  - override hydra/launcher: ray_aws
```
There are several standard approaches for configuring plugins. Check [this page](../patterns/configuring_plugins.md) for more information.

### `ray_aws` launcher

:::important
`ray_aws` launcher is built on top of ray's [autoscaler sdk](https://docs.ray.io/en/releases-1.3.0/cluster/sdk.html). To get started, you need to
[config your AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).
`ray autoscaler sdk` expects your AWS credentials have certain permissions for [`EC2`](https://aws.amazon.com/ec2) and [`IAM`](https://aws.amazon.com/iam). Read [this](https://github.com/ray-project/ray/issues/9327) for more information.
:::

`ray autoscaler sdk` expects a configuration for the EC2 cluster; we've schematized the configs in <GithubLink to="plugins/hydra_ray_launcher/hydra_plugins/hydra_ray_launcher/_config.py">here</GithubLink>

<details>
  <summary>Discover ray_aws launcher's config</summary>

  ```commandline
  $ python my_app.py hydra/launcher=ray_aws --cfg hydra -p hydra.launcher
  # @package hydra.launcher
  _target_: hydra_plugins.hydra_ray_launcher.ray_aws_launcher.RayAWSLauncher
  env_setup:
    pip_packages:
      omegaconf: ${ray_pkg_version:omegaconf}
      hydra_core: ${ray_pkg_version:hydra}
      ray: ${ray_pkg_version:ray}
      cloudpickle: ${ray_pkg_version:cloudpickle}
      pickle5: 0.0.11
      hydra_ray_launcher: 1.1.0.dev3
    commands:
    - conda create -n hydra_${python_version:micro} python=${python_version:micro} -y
    - echo 'export PATH="$HOME/anaconda3/envs/hydra_${python_version:micro}/bin:$PATH"'
      >> ~/.bashrc
  ray:
    init:
      address: null
    remote: {}
    cluster:
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
          key_name: hydra-${oc.env:USER,user}
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
      - ulimit -n 65536;ray start --head --port=6379 --object-manager-port=8076
        --autoscaling-config=~/ray_bootstrap_config.yaml
      worker_start_ray_commands:
      - ray stop
      - ulimit -n 65536; ray start --address=$RAY_HEAD_IP:6379 --object-manager-port=8076
    run_env: auto
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
  logging:
    log_style: auto
    color_mode: auto
    verbosity: 0
  create_update_cluster:
    no_restart: false
    restart_only: false
    no_config_cache: false
  teardown_cluster:
    workers_only: false
    keep_min_workers: false
  ```
</details>


#### Examples

The following examples can be found <GithubLink to="plugins/hydra_ray_launcher/examples">here</GithubLink>.

<details>
  <summary>Simple app</summary>

  ```commandline
  $ python my_app.py --multirun task=1,2,3
  [HYDRA] Ray Launcher is launching 3 jobs,
  [HYDRA]        #0 : task=1
  [HYDRA]        #1 : task=2
  [HYDRA]        #2 : task=3
  [HYDRA] Pickle for jobs: /var/folders/n_/9qzct77j68j6n9lh0lw3vjqcn96zxl/T/tmpqqg4v4i7/job_spec.pkl
  Cluster: default
  ...
  INFO services.py:1172 -- View the Ray dashboard at http://localhost:8265
  (pid=3374) [__main__][INFO] - Executing task 1
  (pid=3374) [__main__][INFO] - Executing task 2
  (pid=3374) [__main__][INFO] - Executing task 3
  ...
  [HYDRA] Stopping cluster now. (stop_cluster=true)
  [HYDRA] Deleted the cluster (provider.cache_stopped_nodes=false)
  Destroying cluster. Confirm [y/N]: y [automatic, due to --yes]
  ...
  No nodes remaining.

  ```
</details>


<details>
  <summary>Upload & Download from remote cluster</summary>

  If your application is dependent on multiple modules, you can configure `hydra.launcher.sync_up` to upload dependency modules to the remote cluster.
  You can also configure `hydra.launcher.sync_down` to download output from remote cluster if needed. This functionality is built on top of `rsync`, `include` and `exclude` is consistent with how it works in `rsync`.

  ```commandline
  $  python train.py --multirun random_seed=1,2,3
  [HYDRA] Ray Launcher is launching 3 jobs,
  [HYDRA]        #0 : random_seed=1
  [HYDRA]        #1 : random_seed=2
  [HYDRA]        #2 : random_seed=3
  [HYDRA] Pickle for jobs: /var/folders/n_/9qzct77j68j6n9lh0lw3vjqcn96zxl/T/tmptdkye9of/job_spec.pkl
  Cluster: default
  ...
  INFO services.py:1172 -- View the Ray dashboard at http://localhost:8265
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
  [HYDRA] Deleted the cluster (provider.cache_stopped_nodes=false)
  Destroying cluster. Confirm [y/N]: y [automatic, due to --yes]
  ...
  No nodes remaining.

  ```
</details>


##### Manage Cluster LifeCycle
You can manage the Ray EC2 cluster lifecycle by configuring the flags provided by the plugin:

- Default setting (no need to specify on commandline): delete cluster after job finishes remotely:
  ```commandline
  hydra.launcher.stop_cluster=true
  hydra.launcher.ray.cluster.provider.cache_stopped_nodes=false
  hydra.launcher.teardown_cluster.workers_only=false
  hydra.launcher.teardown_cluster.keep_min_workers=false
  ```

- Keep cluster running after jobs finishes remotely
  ```commandline
  hydra.launcher.stop_cluster=false
  ```

- Power off EC2 instances and control node termination using `hydra.launcher.ray.cluster.provider.cache_stopped_nodes`
and `hydra.launcher.teardown_cluster.workers_only`

  | cache_stopped_nodes | workers_only | behavior |
  |---------------------|--------------|----------|
  | false | false | All nodes are terminated |
  | false | true | Keeps head node running and terminates only worker node |
  | true | false | Keeps both head node and worker node and stops both of them |
  | true | true | Keeps both head node and worker node and stops only worker node |

- Keep `hydra.launcher.ray.cluster.min_workers` worker nodes
and delete the rest of the worker nodes
  ```commandline
  hydra.launcher.teardown_cluster.keep_min_workers=true
  ```

Additionally, you can configure how to create or update the cluster:

- Default config: run setup commands, restart Ray and use
the config cache if available
  ```commandline
  hydra.launcher.create_update_cluster.no_restart=false
  hydra.launcher.create_update_cluster.restart_only=false
  hydra.launcher.create_update_cluster.no_config_cache=false
  ```

- Skip restarting Ray services when updating the cluster config
  ```commandline
  hydra.launcher.create_update_cluster.no_restart=true
  ```

- Skip running setup commands and only restart Ray (cannot be used with
`hydra.launcher.create_update_cluster.no_restart`)
  ```commandline
  hydra.launcher.create_update_cluster.restart_only=true
  ```

- Fully resolve all environment settings from the cloud provider again
  ```commandline
  hydra.launcher.create_update_cluster.no_config_cache=true
  ```


##### Configure Ray Logging
You can manage Ray specific logging by configuring the flags provided by the plugin:

- Default config: use minimal verbosity and automatically
detect whether to use pretty-print and color mode
  ```commandline
  hydra.launcher.logging.log_style="auto"
  hydra.launcher.logging.color_mode="auto"
  hydra.launcher.logging.verbosity=0
  ```

- Disable pretty-print
  ```commandline
  hydra.launcher.logging.log_style="record"
  ```

- Disable color mode
  ```commandline
  hydra.launcher.logging.color_mode="false"
  ```

- Increase Ray logging verbosity
  ```commandline
  hydra.launcher.logging.verbosity=3
  ```

### `ray` launcher

`ray` launcher lets you launch application on your ray cluster or local machine. You can easily config how your jobs are executed by changing `ray` launcher's configuration here
 `~/hydra/plugins/hydra_ray_launcher/hydra_plugins/hydra_ray_launcher/conf/hydra/launcher/ray.yaml`

 The <GithubLink to="plugins/hydra_ray_launcher/examples/simple">example application</GithubLink> starts a new ray cluster.
```commandline
$ python my_app.py  --multirun hydra/launcher=ray
[HYDRA] Ray Launcher is launching 1 jobs, sweep output dir: multirun/2020-11-10/15-16-28
[HYDRA] Initializing ray with config: {}
INFO services.py:1164 -- View the Ray dashboard at http://127.0.0.1:8266
[HYDRA]        #0 :
(pid=97801) [__main__][INFO] - Executing task 1
```

You can run the example application on your existing ray cluster as well by overriding `hydra.launcher.ray.init.address`:
```commandline
$ python my_app.py  --multirun hydra/launcher=ray hydra.launcher.ray.init.address=localhost:6379'
[HYDRA] Ray Launcher is launching 1 jobs, sweep output dir: multirun/2020-11-10/15-13-32
[HYDRA] Initializing ray with config: {'num_cpus': None, 'num_gpus': None, 'address': 'localhost:6379'}
INFO worker.py:633 -- Connecting to existing Ray cluster at address: 10.30.99.17:6379
[HYDRA]        #0 :
(pid=93358) [__main__][INFO] - Executing task 1
```

### Configure `ray.init()` and `ray.remote()`
Ray launcher is built on top of [`ray.init()`](https://docs.ray.io/en/master/package-ref.html?highlight=ray.remote#ray-init)
and [`ray.remote()`](https://docs.ray.io/en/master/package-ref.html?highlight=ray.remote#ray-remote).
You can configure `ray` by overriding `hydra.launcher.ray.init` and `hydra.launcher.ray.remote`.
Check out an <GithubLink to="plugins/hydra_ray_launcher/examples/simple/config.yaml">example config</GithubLink>.
