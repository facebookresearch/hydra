---
id: callbacks
title: Callbacks
sidebar_label: Callbacks
---

import GithubLink from "@site/src/components/GithubLink"
import {ExampleGithubLink} from "@site/src/components/GithubLink"

<ExampleGithubLink text="Examples" to="hydra/experimental/callbacks.py"/>

The <GithubLink to="hydra/experimental/callback.py">Callback interface</GithubLink> enables custom
code to be triggered by various Hydra events.

To use the callback API, one should import Hydra's `Callback` class:
```python
from hydra.experimental.callback import Callback
```
Users can then create subclasses of this `Callback` class, overriding one or more of
the methods defined by `Callback`. For the methods of a subclass to be called at the
appropriate time, the subclass must be registered with Hydra in the `hydra.callbacks` config
 (see examples below).

The full API exposed by the `hydra.experimental.callback.Callback` class is listed below:

<details>
  <summary>Events supported (Click to expand)</summary>

    ```python
    from hydra.types import TaskFunction

    class Callback:
        def on_run_start(self, config: DictConfig, **kwargs: Any) -> None:
            """
            Called in RUN mode before job/application code starts. `config` is composed with overrides.
            Some `hydra.runtime` configs are not populated yet.
            See hydra.core.utils.run_job for more info.
            """
            ...

        def on_run_end(self, config: DictConfig, **kwargs: Any) -> None:
            """
            Called in RUN mode after job/application code returns.
            """
            ...

        def on_multirun_start(self, config: DictConfig, **kwargs: Any) -> None:
            """
            Called in MULTIRUN mode before any job starts.
            When using a launcher, this will be executed on local machine before any Sweeper/Launcher is initialized.
            """
            ...

        def on_multirun_end(self, config: DictConfig, **kwargs: Any) -> None:
            """
            Called in MULTIRUN mode after all jobs returns.
            When using a launcher, this will be executed on local machine.
            """
            ...

        def on_job_start(self, config: DictConfig, *, task_function: TaskFunction, **kwargs: Any) -> None:
            """
            Called in both RUN and MULTIRUN modes, once for each Hydra job (before running application code).
            This is called from within `hydra.core.utils.run_job`. In the case of remote launching, this will be executed
            on the remote server along with your application code. The `task_function` argument is the function
            decorated with `@hydra.main`.
            """
            ...

        def on_job_end(
            self, config: DictConfig, job_return: JobReturn, **kwargs: Any
        ) -> None:
            """
            Called in both RUN and MULTIRUN modes, once for each Hydra job (after running
            application code).
            This is called from within `hydra.core.utils.run_job`. In the case of remote launching, this will be executed
            on the remote server after your application code.

            `job_return` contains info that could be useful for logging or post-processing.
            See hydra.core.utils.JobReturn for more.
            """
            ...
    ```
</details>

### Configure Callback

Say we have `MyCallback` so after every job ends we can upload a certain file to a S3 bucket.
For simplicity we include this Callback class within the application, in real life you should have the
Callback in a separate file.
Running the application, we can see our custom method `on_job_end` was called.

<div className="row">
<div className="col col--9">

```python title="my_app.py"
class MyCallback(Callback):
   def __init__(self, bucket: str, file_path: str) -> None:
        self.bucket = bucket
        self.file_path = file_path

   def on_job_end(self, config: DictConfig, **kwargs: Any) -> None:
        print(f"Job ended,uploading...")
        # uploading...

@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
```
</div>
<div className="col col--3" >

```commandline title="output"

$ python  my_app.py
foo: bar

Job ended,uploading...











```
</div>
</div>

Now let's take a look at the configurations.

<div className="row">
<div className="col col--4">

```commandline title="$ tree conf"
conf
├── config.yaml
└── hydra
    └── callbacks
        └── my_callback.yaml


```
</div>
<div className="col  col--3">

```commandline title="conf/config.yaml"
defaults:
 - /hydra/callbacks:
    - my_callback

foo: bar


```
</div>
<div className="col  col--5">

```commandline title="conf/hydra/callbacks/my_callback.yaml"
# @package _global_
hydra:
  callbacks:
    my_callback:
      _target_: my_app.MyCallback
      bucket: my_s3_bucket
      file_path: ./test.pt
```
</div>
</div>


### Callback ordering
The `on_run_start` or `on_multirun_start` method will get called first,
followed by `on_job_start` (called once for each job).
After each job `on_job_end` is called, and finally either `on_run_end` or
`on_multirun_end` is called one time before the application exits.

In the `hydra.callbacks` section of your config, you can use a list to register multiple callbacks. They will be called in the final composed order for `start` events and
in reversed order for `end` events. So, for example, suppose we have the following composed config:
```commandline title="python my_app.py --cfg hydra -p hydra.callbacks"
# @package hydra.callbacks
my_callback1:
  _target_: my_app.MyCallback1
  param1: val1
my_callback2:
  _target_: my_app.MyCallback2
  param2: val2
```
Before each job starts, `MyCallback1.on_job_start` will get called first,
followed by `MyCallback2.on_job_start`.
After each job ends, `MyCallback2.on_job_end` will get called first,
followed by `MyCallback1.on_job_end`.


### Example callbacks

We've included some example callbacks  <GithubLink to="hydra/experimental/callbacks.py">here</GithubLink>:
- `LogJobReturnCallback` is especially useful for logging errors when running on a remote cluster (e.g. slurm.)
- `PickleJobInfoCallback` can be used to reproduce a Hydra job. See [here](/experimental/rerun.md) for more.
