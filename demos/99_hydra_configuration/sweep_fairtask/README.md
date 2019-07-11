# Customizing  Fairtask

Hydra can use fairtask to launch jobs.
The fairtsk configuration is specific to your job, specifically in things like number of required
CPUs, GPUs, RAM and number of jobs to run concurrently.
See [fairtask](https://github.com/fairinternal/fairtask) and 
[fairtask-slurm](https://github.com/fairinternal/fairtask-slurm/blob/master/docs/SLURMQueueConfig.schema.md) 
for more information about fairtask. 

launcher/fairtask.yaml:
```yaml
hydra:
  launcher:
    class: hydra.launchers.FAIRTaskLauncher
    params:
      # debug launching issues, set to true to run workers in the same process.
      no_workers: false
      queue: slurm
      queues:
        local:
          class: fairtask.local.LocalQueueConfig
          params:
            num_workers: 2
        slurm:
          class: fairtask_slurm.slurm.SLURMQueueConfig
          params:
            num_jobs: ${hydra:num_jobs}
            num_nodes_per_job: 1
            num_workers_per_node: 1
            name: ${hydra.name}
            maxtime_mins: 4320
            partition: learnfair
            cpus_per_worker: 10
            mem_gb_per_worker: 64
            gres: 'gpu:1'
            log_directory: ${hydra.sweep.dir}/.slurm
            output: slurm-%j.out
            error: slurm-%j.err
```
You can override hydra related parameters from the command line, for example this would switch fairtask
to use the local queue.
```bash
python demos/99_hydra_configuration/sweep_fairtask/main.py -s param=1,2 hydra.launcher.params.queue=local
Sweep output dir : /checkpoint/omry/outputs/2019-07-10_18-40-35
Launching 2 jobs to local queue
        #0 : param=1
        #1 : param=2
Dask dashboard for "local" at http://localhost:8007.
[2019-07-10 18:40:37,666][hydra.utils][INFO] - Setting job:num=0
[2019-07-10 18:40:37,667][hydra.utils][INFO] - Setting job:name=main
[2019-07-10 18:40:37,667][hydra.utils][INFO] - Setting job:id=unknown
[2019-07-10 18:40:37,667][hydra.utils][INFO] - Setting job:override_dirname=param:1
[2019-07-10 18:40:37,678][__main__][INFO] - Running on: devfair0260
param: 1

[2019-07-10 18:40:37,793][hydra.utils][INFO] - Setting job:num=1
[2019-07-10 18:40:37,794][hydra.utils][INFO] - Setting job:name=main
[2019-07-10 18:40:37,794][hydra.utils][INFO] - Setting job:id=unknown
[2019-07-10 18:40:37,794][hydra.utils][INFO] - Setting job:override_dirname=param:2
[2019-07-10 18:40:37,834][__main__][INFO] - Running on: devfair0260
param: 2
```

