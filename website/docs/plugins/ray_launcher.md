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
 `ray_aws` launches jobs remotely on AWS and is built on top of [Ray cluster launcher](https://docs.ray.io/en/latest/cluster/launcher.html). `ray` launches jobs on your local machine or existing ray cluster. 

### Installation

```commandline
$ pip install hydra-ray-launcher --pre
```

### Usage
Once installed, add `hydra/launcher=ray_aws` or `hydra/launcher=ray` to your command line. Alternatively, override `hydra/launcher` in your config:

```yaml
defaults:
  - override hydra/launcher: ray_aws
```


### `ray_aws` launcher

:::important
`ray_aws` launcher is built on top of ray's [cluster launcher cli](https://docs.ray.io/en/latest/cluster/launcher.html). To get started, you need to 
[config your AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).
`ray cluster launcher` expects your AWS credentials have certain permissions for [`EC2`](https://aws.amazon.com/ec2) and [`IAM`](https://aws.amazon.com/iam). Read [this](https://github.com/ray-project/ray/issues/9327) for more information.
:::

`ray cluster launcher` expects a yaml file to provide configuration for the EC2 cluster; we've schematized the configs in <GithubLink to="plugins/hydra_ray_launcher/hydra_plugins/hydra_ray_launcher/_config.py">here</GithubLink>

<details><summary>Discover ray_aws launcher's config</summary>

```commandline
$ python my_app.py hydra/launcher=ray_aws --cfg hydra -p hydra.launcher
# @package hydra.launcher
_target_: hydra_plugins.hydra_ray_launcher.ray_aws_launcher.RayAWSLauncher
env_setup:
  pip_packages:
    omegaconf: 2.0.5
    hydra_core: 1.0.4
    ray: 1.0.1.post1
    cloudpickle: 1.6.0
    pickle5: 0.0.11
    hydra_ray_launcher: 0.1.2
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

The following examples can be found <GithubLink to="plugins/hydra_ray_launcher/examples">here</GithubLink>.

<details><summary>Simple app</summary>

```commandline
$ python my_app.py --multirun task=1,2,3
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

<details><summary>Dockerized app</summary>

```commandline
$ python docker_app.py --multirun hydra/launcher=ray_aws task=1,2,3

[2021-02-19 11:08:09,807][HYDRA] Ray Launcher is launching 3 jobs, 
[2021-02-19 11:08:09,808][HYDRA] 	#0 : task=1
[2021-02-19 11:08:09,874][HYDRA] 	#1 : task=2
[2021-02-19 11:08:09,952][HYDRA] 	#2 : task=3
[2021-02-19 11:08:10,043][HYDRA] Pickle for jobs: /var/folders/4k/ptbs25l170389035l24w1x7c0000gr/T/tmptgz3d3vf/job_spec.pkl
[2021-02-19 11:08:10,047][HYDRA] Saving RayClusterConf in a temp yaml file: /var/folders/4k/ptbs25l170389035l24w1x7c0000gr/T/tmpoz5uo0ji.yaml.
[2021-02-19 11:08:10,050][HYDRA] Running command: ray up -y /var/folders/4k/ptbs25l170389035l24w1x7c0000gr/T/tmpoz5uo0ji.yaml
[2021-02-19 11:12:30,502][HYDRA] Output: 18:09:31 up 0 min,  1 user,  load average: 4.26, 1.13, 0.39
Using default tag: latest
latest: Pulling from samuelstanton/ray-plugin-example
d519e2592276: Pull complete 
d22d2dfcfa9c: Pull complete 
b3afe92c540b: Pull complete 
16d86eee720b: Pull complete 
5963dd09a569: Pull complete 
96011bf4bfd6: Pull complete 
3df5cb5c705d: Pull complete 
1954c691420e: Pull complete 
86a9e946bc21: Pull complete 
2412615f18bb: Pull complete 
b452d0e13d34: Pull complete 
4f4fb700ef54: Pull complete 
522ac083fde5: Pull complete 
68e6ba2455e1: Pull complete 
32371fe2d681: Pull complete 
Digest: sha256:b1faf41befceb3ece50a5192c5a112803bd1252cdaa9de0bf8e4cb052ffead61
Status: Downloaded newer image for samuelstanton/ray-plugin-example:latest
docker.io/samuelstanton/ray-plugin-example:latest
3aef14452ace7d89607df35fe61bffbbcfcb332d1aab5046cb8c49cc8a2e895b
Did not find any active Ray processes.
Local node IP: 172.31.17.39
2021-02-19 18:12:27,336	INFO services.py:1171 -- View the Ray dashboard at http://localhost:8265

--------------------
Ray runtime started.
--------------------

Next steps
  To connect to this Ray runtime from another node, run
    ray start --address='172.31.17.39:6379' --redis-password='5241590000000000'
  
  Alternatively, use the following Python code:
    import ray
    ray.init(address='auto', _redis_password='5241590000000000')
  
  If connection fails, check your firewall settings and network configuration.
  
  To terminate the Ray runtime, run
    ray stop
Cluster: example-cluster

Checking AWS environment settings
AWS config
  IAM Profile: ray-head-v1
  EC2 Key pair (head & workers): hydra [default]
  VPC Subnets (head & workers): subnet-7df0af07, subnet-db16f7b0 [default]
  EC2 Security groups (head & workers): sg-0cf61dce64b65dad4 [default]
  EC2 AMI (head & workers): ami-010bc10395b6826fb

No head node found. Launching a new cluster. Confirm [y/N]: y [automatic, due to --yes]

Acquiring an up-to-date head node
  Launched 1 nodes [subnet_id=subnet-7df0af07]
    Launched instance i-08a43e4e17395aefe [state=pending, info=pending]
  Launched a new head node
  Fetching the new head node
  
<1/1> Setting up head node
  Prepared bootstrap config
  New status: waiting-for-ssh
  [1/7] Waiting for SSH to become available
    Running `uptime` as a test.
    Waiting for IP
      Not yet available, retrying in 10 seconds
      Not yet available, retrying in 10 seconds
      Received: 3.16.129.84
    SSH still not available (SSH command failed.), retrying in 5 seconds.
    SSH still not available (SSH command failed.), retrying in 5 seconds.
    SSH still not available (SSH command failed.), retrying in 5 seconds.
    SSH still not available (SSH command failed.), retrying in 5 seconds.
    Success.
  Updating cluster configuration. [hash=4d34ba352ab497b21ff26839065a5434dbde0096]
  New status: syncing-files
  [2/7] Processing file mounts
  [3/7] No worker file mounts to sync
  New status: setting-up
  [4/7] No initialization commands to run.
  [5/7] Initalizing command runner
  [6/7] No setup commands to run.
  [7/7] Starting the Ray runtime
  New status: up-to-date

Useful commands
  Monitor autoscaling with
    ray exec /var/folders/4k/ptbs25l170389035l24w1x7c0000gr/T/tmpoz5uo0ji.yaml 'tail -n 100 -f /tmp/ray/session_latest/logs/monitor*'
  Connect to a terminal on the cluster head:
    ray attach /var/folders/4k/ptbs25l170389035l24w1x7c0000gr/T/tmpoz5uo0ji.yaml
  Get a remote shell to the cluster manually:
    ssh -tt -o IdentitiesOnly=yes -i /Users/stantsa/.ssh/hydra.pem ubuntu@3.16.129.84 docker exec -it hydra-container /bin/bash 
 Error: ssh: connect to host 3.16.129.84 port 22: Operation timed out
ssh: connect to host 3.16.129.84 port 22: Operation timed out
ssh: connect to host 3.16.129.84 port 22: Operation timed out
ssh: connect to host 3.16.129.84 port 22: Connection refused
Warning: Permanently added '3.16.129.84' (ECDSA) to the list of known hosts.
Shared connection to 3.16.129.84 closed.
Shared connection to 3.16.129.84 closed.
Shared connection to 3.16.129.84 closed.
Shared connection to 3.16.129.84 closed.
Shared connection to 3.16.129.84 closed.
Shared connection to 3.16.129.84 closed.
Shared connection to 3.16.129.84 closed.
Shared connection to 3.16.129.84 closed.
Shared connection to 3.16.129.84 closed.
Shared connection to 3.16.129.84 closed.
Shared connection to 3.16.129.84 closed.
Shared connection to 3.16.129.84 closed.
Shared connection to 3.16.129.84 closed.
Shared connection to 3.16.129.84 closed.
Shared connection to 3.16.129.84 closed.
[2021-02-19 11:12:30,524][HYDRA] Running command: ray exec --run-env=auto /var/folders/4k/ptbs25l170389035l24w1x7c0000gr/T/tmpoz5uo0ji.yaml echo $(mktemp -d)
[2021-02-19 11:12:32,899][HYDRA] Output: /tmp/tmp.Uaxh9rdIEl
Loaded cached provider configuration
If you experience issues with the cloud provider, try re-running the command with --no-config-cache.
Fetched IP: 3.16.129.84 
 Error: Shared connection to 3.16.129.84 closed.
[2021-02-19 11:12:32,899][HYDRA] Created temp path on remote server /tmp/tmp.Uaxh9rdIEl
[2021-02-19 11:12:32,902][HYDRA] Running command: ray rsync-up /var/folders/4k/ptbs25l170389035l24w1x7c0000gr/T/tmpoz5uo0ji.yaml /var/folders/4k/ptbs25l170389035l24w1x7c0000gr/T/tmptgz3d3vf/ /tmp/tmp.Uaxh9rdIEl
[2021-02-19 11:12:36,056][HYDRA] Output: Loaded cached provider configuration
If you experience issues with the cloud provider, try re-running the command with --no-config-cache.
Fetched IP: 3.16.129.84 
 Error: Shared connection to 3.16.129.84 closed.
[2021-02-19 11:12:36,059][HYDRA] Running command: ray rsync-up /var/folders/4k/ptbs25l170389035l24w1x7c0000gr/T/tmpoz5uo0ji.yaml /Users/stantsa/code/hydra/plugins/hydra_ray_launcher/hydra_plugins/hydra_ray_launcher/_remote_invoke.py /tmp/tmp.Uaxh9rdIEl/_remote_invoke.py
[2021-02-19 11:12:39,204][HYDRA] Output: Loaded cached provider configuration
If you experience issues with the cloud provider, try re-running the command with --no-config-cache.
Fetched IP: 3.16.129.84 
 Error: Shared connection to 3.16.129.84 closed.
[2021-02-19 11:12:39,207][HYDRA] Running command: ray exec --run-env=auto /var/folders/4k/ptbs25l170389035l24w1x7c0000gr/T/tmpoz5uo0ji.yaml python /tmp/tmp.Uaxh9rdIEl/_remote_invoke.py /tmp/tmp.Uaxh9rdIEl
[2021-02-19 11:12:53,344][HYDRA] Output: 2021-02-19 18:12:42,771	INFO services.py:1171 -- View the Ray dashboard at http://127.0.0.1:8266
(pid=279) [2021-02-19 18:12:47,990][__main__][INFO] - Executing task 2
(pid=280) [2021-02-19 18:12:48,032][__main__][INFO] - Executing task 1
(pid=279) [2021-02-19 18:12:49,148][__main__][INFO] - Executing task 3
Loaded cached provider configuration
If you experience issues with the cloud provider, try re-running the command with --no-config-cache.
Fetched IP: 3.16.129.84 
 Error: Shared connection to 3.16.129.84 closed.
[2021-02-19 11:12:53,347][HYDRA] Running command: ray rsync-down /var/folders/4k/ptbs25l170389035l24w1x7c0000gr/T/tmpoz5uo0ji.yaml /tmp/tmp.Uaxh9rdIEl/returns.pkl /var/folders/4k/ptbs25l170389035l24w1x7c0000gr/T/tmp93p0j1q1
[2021-02-19 11:12:55,858][HYDRA] Output: Loaded cached provider configuration
If you experience issues with the cloud provider, try re-running the command with --no-config-cache.
Fetched IP: 3.16.129.84 
 Error: 
[2021-02-19 11:12:55,861][HYDRA] Running command: ray exec --run-env=auto /var/folders/4k/ptbs25l170389035l24w1x7c0000gr/T/tmpoz5uo0ji.yaml rm -rf /tmp/tmp.Uaxh9rdIEl
[2021-02-19 11:12:57,877][HYDRA] Output: Loaded cached provider configuration
If you experience issues with the cloud provider, try re-running the command with --no-config-cache.
Fetched IP: 3.16.129.84 
 Error: Shared connection to 3.16.129.84 closed.
[2021-02-19 11:12:57,877][HYDRA] Stopping cluster now. (stop_cluster=true)
[2021-02-19 11:12:57,878][HYDRA] Deleted the cluster (provider.cache_stopped_nodes=false)
[2021-02-19 11:12:57,880][HYDRA] Running command: ray down -y /var/folders/4k/ptbs25l170389035l24w1x7c0000gr/T/tmpoz5uo0ji.yaml
[2021-02-19 11:13:07,004][HYDRA] Output: Stopped all 13 Ray processes.
hydra-container
Loaded cached provider configuration
If you experience issues with the cloud provider, try re-running the command with --no-config-cache.
Destroying cluster. Confirm [y/N]: y [automatic, due to --yes]
Fetched IP: 3.16.129.84
Fetched IP: 3.16.129.84
Requested 1 nodes to shut down. [interval=1s]
0 nodes remaining after 5 second(s).
No nodes remaining. 
 Error: Shared connection to 3.16.129.84 closed.
Shared connection to 3.16.129.84 closed.
```
</details>

##### Manage Cluster LifeCycle
You can manage the Ray EC2 cluster lifecycle by configuring the two flags provided by the plugin:

- Default setting (no need to specify on commandline): Delete cluster after job finishes remotely:
```commandline
hydra.launcher.stop_cluster=true
hydra.launcher.ray.cluster.provider.cache_stopped_nodes=False
```

- Keep cluster running after jobs finishes remotely
```commandline
hydra.launcher.stop_cluster=False
```

- Power off EC2 instances without deletion
```commandline
hydra.launcher.ray.cluster.provider.cache_stopped_nodes=true
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


### Using Docker with AWS
If you have a docker container publicly hosted, you can launch containerized jobs with only a 
minimal change to the config. Note that the Amazon EC2 AMI will need 
to have Docker already installed.

<details><summary>Example config for dockerized app</summary>

```
hydra:
  launcher:
    _target_: hydra_plugins.hydra_ray_launcher.ray_aws_launcher.RayAWSLauncher
    env_setup:
      pip_packages:
        omegaconf: null
        hydra_core: null
        ray: null
        cloudpickle: null
        pickle5: null
        hydra_ray_launcher: null
      commands: []
    ray:
      cluster:
        cluster_name: example-cluster
        min_workers: 0
        max_workers: 0
        initial_workers: 0
        autoscaling_mode: default
        target_utilization_fraction: 0.8
        idle_timeout_minutes: 5
        docker:
          image: 'samuelstanton/ray-plugin-example'
          container_name: 'hydra-container'
          pull_before_run: true
          run_options: []
        provider:
          type: aws
          region: us-east-2
          availability_zone: us-east-2a,us-east-2b
        auth:
          ssh_user: ubuntu
        head_node:
          InstanceType: m4.large
          ImageId: ami-010bc10395b6826fb
        worker_nodes:
          InstanceType: m4.large
          ImageId: ami-010bc10395b6826fb
    stop_cluster: true
```
</details>
