---
id: rq_launcher
title: RQ Launcher plugin
sidebar_label: RQ Launcher plugin
---
[![PyPI](https://img.shields.io/pypi/v/hydra-rq-launcher)](https://pypi.org/project/hydra-rq-launcher/)
![PyPI - License](https://img.shields.io/pypi/l/hydra-rq-launcher)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hydra-rq-launcher)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/hydra-rq-launcher.svg)](https://pypistats.org/packages/hydra-rq-launcher)
[![Example application](https://img.shields.io/badge/-Example%20application-informational)](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_rq_launcher/example)
[![Plugin source](https://img.shields.io/badge/-Plugin%20source-informational)](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_rq_launcher)

The RQ Launcher plugin provides a launcher for distributed execution and job queuing based on [Redis Queue (RQ)](https://python-rq.org).

RQ launcher allows parallelizing across multiple nodes and scheduling jobs in queues. Usage of this plugin requires a [Redis server](https://redis.io/topics/quickstart). When parallelisation on a single node is intended, the Joblib launcher may be preferable, since it works without a database.


### Installation
```commandline
pip install hydra-rq-launcher --upgrade
```
Usage of this plugin requires a [Redis server](https://redis.io/topics/quickstart).

Note that RQ does [not support Windows](https://python-rq.org/docs/#limitations).

### Usage
Once installed, add `hydra/launcher=rq` to your command line. Alternatively, override `hydra/launcher` in your config:

```yaml
defaults:
  - override hydra/launcher: rq
```

The configuration packaged with the plugin is defined [here](https://github.com/facebookresearch/hydra/blob/master/plugins/hydra_rq_launcher/hydra_plugins/hydra_rq_launcher/config.py). The default configuration is as follows:

```yaml title="$ python your_app.py hydra/launcher=rq --cfg hydra -p hydra.launcher"
# @package hydra.launcher
_target_: hydra_plugins.hydra_rq_launcher.rq_launcher.RQLauncher
enqueue:
  job_timeout: null                  # maximum runtime of the job before it's killed (e.g. "1d" for 1 day, units: d/h/m/s), default: no limit
  ttl: null                          # maximum queued time before the job before is discarded (e.g. "1d" for 1 day, units: d/h/m/s), default: no limit
  result_ttl: null                   # how long successful jobs and their results are kept (e.g. "1d" for 1 day, units: d/h/m/s), default: no limit
  failure_ttl: null                  # specifies how long failed jobs are kept (e.g. "1d" for 1 day, units: d/h/m/s), default: no limit
  at_front: false                    # place job at the front of the queue, instead of the back
  job_id: null                       # job id, will be overidden automatically by a uuid unless specified explicitly
  description: null                  # description, will be overidden automatically unless specified explicitly
queue: default                       # queue name
redis:
  host: ${env:REDIS_HOST,localhost}  # host address via REDIS_HOST environment variable, default: localhost
  port: ${env:REDIS_PORT,6379}       # port via REDIS_PORT environment variable, default: 6379
  db: ${env:REDIS_DB,0}              # database via REDIS_DB environment variable, default: 0
  password: ${env:REDIS_PASSWORD,}   # password via REDIS_PASSWORD environment variable, default: no password
  mock: ${env:REDIS_MOCK,False}      # switch to run without redis server in single thread, for testing purposes only
stop_after_enqueue: false            # stop after enqueueing by raising custom exception
wait_polling: 1.0                    # wait time in seconds when polling results
```

The plugin is using environment variables to store Redis connection information. The environment variables `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`, and `REDIS_PASSWORD`, are used for the host address, port, database, and password of the server, respectively.

For example, they might be set as follows when using `bash` or `zsh` as a shell:

```commandline
export REDIS_HOST="localhost"
export REDIS_PORT="6379"
export REDIS_DB="0"
export REDIS_PASSWORD=""
```

Assuming configured environment variables, workers connecting to the Redis server can be launched using:

```commandline
rq worker --url redis://:$REDIS_PASSWORD@$REDIS_HOST:$REDIS_PORT/$REDIS_DB
```

An [example application](https://github.com/facebookresearch/hydra/tree/master/plugins/hydra_rq_launcher/example) using this launcher is provided in the plugin repository.

Starting the app with `python my_app.py --multirun task=1,2,3,4,5` will enqueue five jobs to be processed by worker instances:

```text
$ python my_app.py --multirun task=1,2,3,4,5

[HYDRA] RQ Launcher is enqueuing 5 job(s) in queue : default
[HYDRA] Sweep output dir : multirun/2020-06-15/18-00-00
[HYDRA] Enqueued 13b3da4e-03f7-4d16-9ca8-cfb3c48afeae
[HYDRA] 	#1 : task=1
[HYDRA] Enqueued 00c6a32d-e5a4-432c-a0f3-b9d4ef0dd585
[HYDRA] 	#2 : task=2
[HYDRA] Enqueued 63b90f27-0711-4c95-8f63-70164fd850df
[HYDRA] 	#3 : task=3
[HYDRA] Enqueued b1d49825-8b28-4516-90ca-8106477e1eb1
[HYDRA] 	#4 : task=4
[HYDRA] Enqueued ed96bdaa-087d-4c7f-9ecb-56daf948d5e2
[HYDRA] 	#5 : task=5
[HYDRA] Finished enqueuing
[HYDRA] Polling job statuses every 1.0 sec
```

Note that any dependencies need to be installed in the Python environment used to run the RQ worker. For serialization of jobs [`cloudpickle`](https://github.com/cloudpickle/cloudpickle) is used.

The [RQ documentation](https://python-rq.org/) holds further information on [job monitoring](http://python-rq.org/docs/monitoring/), which can be done via console or [web interfaces](https://github.com/nvie/rq-dashboard), and provides [patterns](https://python-rq.org/patterns/) for worker and exception handling.
