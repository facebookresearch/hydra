---
id: rerun
title: Re-run a job from previous config
sidebar_label: Re-run 
---

import {ExampleGithubLink} from "@site/src/components/GithubLink"

<ExampleGithubLink text="Example application" to="examples/experimental/rerun"/>

:::caution
This is an experimental feature. Please read through this page to understand what is supported.
:::

We use the example app linked above for demonstration. To save the configs for re-run, first use the experimental
Hydra Callback for saving the job info:


```yaml title="config.yaml"
hydra:
  callbacks:
    save_job_info:
      _target_: hydra.experimental.pickle_job_info_callback.PickleJobInfoCallback
```




```python title="Example function"
@hydra.main(config_path=".", config_name="config")
def my_app(cfg: DictConfig) -> None:
    log.info(f"output_dir={HydraConfig.get().runtime.output_dir}")
    log.info(f"cfg.foo={cfg.foo}")
```


Run the example app:
```commandline
$ python my_app.py
[2022-03-16 14:51:30,905][hydra.experimental.pickle_job_info_callback][INFO] - Saving job configs in /Users/jieru/workspace/hydra/examples/experimental/outputs/2022-03-16/14-51-30/.hydra/config.pickle
[2022-03-16 14:51:30,906][__main__][INFO] - Output_dir=/Users/jieru/workspace/hydra/examples/experimental/outputs/2022-03-16/14-51-30
[2022-03-16 14:51:30,906][__main__][INFO] - cfg.foo=bar
[2022-03-16 14:51:30,906][hydra.experimental.pickle_job_info_callback][INFO] - Saving job_return in /Users/jieru/workspace/hydra/examples/experimental/outputs/2022-03-16/14-51-30/.hydra/job_return.pickle
```
The Callback saves `config.pickle` in `.hydra` sub dir, this is what we will use for rerun.

Now rerun the app
```commandline
$ OUTPUT_DIR=/Users/jieru/workspace/hydra/examples/experimental/outputs/2022-03-16/14-51-30/.hydra/
$ python my_app.py --experimental-rerun $OUTPUT_DIR/config.pickle
/Users/jieru/workspace/hydra/hydra/main.py:23: UserWarning: Experimental rerun CLI option.
  warnings.warn(msg, UserWarning)
[2022-03-16 14:59:21,666][__main__][INFO] - Output_dir=/Users/jieru/workspace/hydra/examples/experimental/outputs/2022-03-16/14-51-30
[2022-03-16 14:59:21,666][__main__][INFO] - cfg.foo=bar
```
You will notice `my_app.log` is updated with the logging from the second run, but Callbacks are not called this time. Read on to learn more.


### Important Notes
This is an experimental feature. Please reach out if you have any question. 
- Only single run is supported.
- `--experimental-rerun` cannot be used with other command-line options or overrides. They will simply be ignored.
- Rerun passes in a cfg_passthrough directly to your application, this means except for logging, no other `hydra.main` 
functions are called (such as change working dir, or calling callbacks.) 
- The configs are preserved and reconstructed to the best efforts. Meaning we can only guarantee that the `cfg` object 
itself passed in by `hydra.main` stays the same across runs. However, configs are resolved lazily. Meaning we cannot 
guarantee your application will behave the same if your application resolves configs during run time. In the following example,
`cfg.time_now` will resolve to different value every run.

<div className="row">
<div className="col  col--5">

```yaml title="config.yaml"
time_now: ${now:%H-%M-%S}



```

</div>

<div className="col col--7">

```python title="Example function"
@hydra.main(config_path=".", config_name="config")
def my_app(cfg: DictConfig) -> None:
    val = cfg.time_now
    # the rest of the application
```
</div>
</div>
