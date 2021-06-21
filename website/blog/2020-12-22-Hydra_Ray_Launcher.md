---
title: Hydra Ray Launcher
author: Jieru Hu
author_url: https://github.com/jieru-hu
author_image_url: https://graph.facebook.com/733244046/picture/?height=200&width=200
tags: [Hydra, Ray, Plugin]
image: /img/Hydra-Readme-logo2.svg
---

We are happy to announce that we are adding a [Ray Launcher](https://hydra.cc/docs/plugins/ray_launcher) to the Hydra Launchers family. 
Hydra's Launcher plugins enable launching to different environments without changing your existing workflows or application code.
The Hydra Ray Launcher can be used to launch your application to a new or existing [Ray cluster](https://docs.ray.io/en/master/cluster/launcher.html), 
locally or on AWS. In this post we demonstrate the major functionalities of the Launcher. 
For more details on installation and configuration, please check out the [Hydra Ray Launcher documentation](https://hydra.cc/docs/plugins/ray_launcher/). 
As always, please [join our community](https://github.com/facebookresearch/hydra#community) and give us feedback!
<!--truncate-->


[Ray](https://github.com/ray-project/ray) is a simple yet powerful Python library for parallel and distributed programming. Among the many features it provides, Ray comes with a 
 [cluster launcher](https://docs.ray.io/en/master/cluster/launcher.html#ref-automatic-cluster) that can be used to provision resources and start a Ray cluster on top of them. 
Hydra Ray Launcher is built on top of the [Ray Tasks API](https://docs.ray.io/en/master/ray-overview/index.html#parallelizing-python-java-functions-with-ray-tasks) and the Ray cluster launcher. 


### Launching to a new or existing AWS cluster
Hydra Ray Launcher simplifies your experience by allowing the Ray cluster setup to be 
configured transparently by Hydra (eliminating the need for an external YAML file while maintaining 
the flexibility). Hydra Ray Launcher comes with reasonable default configurations which can be found 
[here](https://hydra.cc/docs/plugins/ray_launcher/#ray_aws-launcher) (under the heading, “Discover ray_aws launcher's config”). You can override them in your application
 config or from the command line to fit your use case. 
 The following Ray Launcher example code (e.g., my_app.py) is runnable and can be found [here](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_ray_launcher/examples/simple). 

Launch your Hydra application to AWS by simply overriding: `hydra/launcher=ray_aws`:

```commandline
$ python my_app.py hydra/launcher=ray_aws task=1,2 --multirun
[HYDRA] Ray Launcher is launching 2 jobs, 
[HYDRA]        #0 : task=1
[HYDRA]        #1 : task=2
...
[HYDRA] Running command: ['ray', 'up', '-y', '/var/folders/n_/9qzct77j68j6n9lh0lw3vjqcn96zxl/T/tmp20qvoy15.yaml']
[HYDRA] Output: INFO services.py:1090 -- View the Ray dashboard at http://127.0.0.1:8265
(pid=3823)[__main__][INFO] - Executing task 1
(pid=3822)[__main__][INFO] - Executing task 2
[HYDRA] Stopping cluster now. (stop_cluster=true)
[HYDRA] Deleted the cluster (provider.cache_stopped_nodes=false)
[HYDRA] Running command: ['ray', 'down', '-y', '/var/folders/n_/9qzct77j68j6n9lh0lw3vjqcn96zxl/T/tmpfm2ems9v.yaml']
```

### Launching to a new local Ray Cluster
If you want to do a quick local test, 
you can spin up a local Ray cluster at application run time by specifying `hydra/launcher=ray`. 
In this example, we create a new Ray cluster at application time. 
```commandline
$ python my_app.py  --multirun hydra/launcher=ray 
[HYDRA] Ray Launcher is launching 1 jobs, sweep output dir: multirun/2020-12-17/16-11-28
[HYDRA] Initializing ray with config: {'address': None}
2020-12-17 16:11:29,340 INFO services.py:1090 -- View the Ray dashboard at http://127.0.0.1:8265
[HYDRA]        #0 : 
(pid=62642) [__main__][INFO] - Executing task 1
```
### Launching to an existing local Ray Cluster
You can launch the application on an existing local Ray cluster by configuring the cluster address
 and overriding `hydra/launcher=ray`. In the following example we configure the Ray cluster address
  to local ray cluster and Hydra Ray Launcher was able to connect to the existing Ray cluster and 
  execute the application code:
```commandline
$ python my_app.py  --multirun hydra/launcher=ray hydra.launcher.ray.init.address=localhost:6379
[HYDRA] Ray Launcher is launching 1 jobs, sweep output dir: multirun/2020-11-10/15-13-32
[HYDRA] Initializing ray with config: {'num_cpus': None, 'num_gpus': None, 'address': 'localhost:6379'}
INFO worker.py:633 -- Connecting to existing Ray cluster at address: 10.30.99.17:6379
[HYDRA]        #0 :
(pid=93358) [__main__][INFO] - Executing task 1
```

Hydra Ray Launcher is built on top of Hydra 1.0 and you have access to all of the benefits Hydra brings:

### Parameter sweeps and optimization
Hyperparameter sweeps are common in machine learning research. 
Hydra has built-in grid search and provides several Sweeper plugins for hyperparameter optimization.
 Sweepers can be used together with Launchers for sweeping on different computing platforms. 
 Start from our documentation [here](https://hydra.cc/docs/tutorials/basic/running_your_app/multi-run/) to find more.

### Config type safety
Modern Hydra applications and Hydra Plugins leverage Structured Configs for config validation,
 and Hydra Ray Launcher is no exception. In the following example, we try to override the Ray cluster’s 
 autoscaling mode with an illegal value:

```commandline
$ python my_app.py --multirun hydra.launcher.ray.cluster.autoscaling_mode=foo
Error merging override hydra.launcher.ray.cluster.autoscaling_mode=foo
Invalid value 'foo', expected one of [default, aggressive]
        full_key: hydra.launcher.ray.cluster.autoscaling_mode
        reference_type=RayClusterConf
        object_type=RayClusterConf

Set the environment variable HYDRA_FULL_ERROR=1 for a complete stack trace.
```

That’s it for now! Please try out the new Hydra Ray Launcher and let us know what you think. 
We are always happy to connect with you via [GitHub](https://github.com/facebookresearch/hydra) or the [Hydra Chat](https://hydra-framework.zulipchat.com/).


