# Customizing  submitit

Hydra can use submitit to launch jobs.
The submitit configuration is specific to your job, specifically in things like number of required
CPUs, GPUs, RAM and number of jobs to run concurrently.
See the [submitit repo](https://github.com/fairinternal/submitit) for more information
launcher/submitit.yaml:
```yaml
hydra:
  launcher:
    class: hydra.launchers.SubmititLauncher
    params:
      # one of auto,local,slurm and chronos
      queue: slurm

      folder: ${hydra.sweep.dir}/.${hydra.launcher.params.queue}
      queue_parameters:
        # slrum queue parameters
        slurm:
          nodes: 1
          num_gpus: 1
          ntasks_per_node: 1
          mem: ${hydra.launcher.mem_limit}GB
          cpus_per_task: 10
          time: 60
          partition: learnfair
          signal_delay_s: 120
        # chronos queue parameters
        chronos:
          # See crun documentation for most parameters
          # https://our.internmc.facebook.com/intern/wiki/Chronos-c-binaries/crun/
          hostgroup: blearner_ash_bigsur_fair
          cpu: 10
          mem: ${hydra.launcher.mem_limit}
          gpu: 1
        # local queue parameters
        local:
          gpus_per_node: 1
          tasks_per_node: 1
          timeout_min: 60

    # variables used by various queues above
    mem_limit: 24
```

```text
$ python demos/99_hydra_configuration/sweep_submitit/sweep.py -s param=1,2
[2019-07-10 19:59:42,613][hydra.utils][INFO] - Setting HydraRuntime:num_jobs=2
Sweep output dir : /checkpoint/omry/outputs/2019-07-10_19-59-42
        #0 : param=1
        #1 : param=2
```