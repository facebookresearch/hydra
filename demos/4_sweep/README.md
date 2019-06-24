# Parameter sweeps
Hydra supports running jobs against a distributed system like slurm using fairtask.
To use it, you need to drop in a hydra.yaml file into your config directory.

Among other things, hydra.yaml is configuring the fairtask launcher.
It also controls the job output directory when running normally or on the cluster.

```yaml
hydra:
  run_dir: ./outputs/${now:%Y-%m-%d_%H-%M-%S}
  sweep_dir: /checkpoint/${env:USER}/outputs/${now:%Y-%m-%d_%H-%M-%S}/
  # populated by hydra at runtime
  job_cwd: ???
  # job name, populated by hydra at runtime based on the filename of the hydra.main()
  name: hydra # TODO: this should be ??? but OmegaConf bug prevents it.
  launcher:
    queue: slurm
    # number of concurrent jobs
    concurrent: ???
    queues:
      local:
        class: fairtask.local.LocalQueueConfig
        params:
          num_workers: 2
      slurm:
        class: fairtask_slurm.slurm.SLURMQueueConfig
        params:
          num_jobs: ${hydra.launcher.concurrent}
          num_nodes_per_job: 1
          num_workers_per_node: 1
          name: ${hydra.name}
          maxtime_mins: 4320
          partition: learnfair
          cpus_per_worker: 10
          mem_gb_per_worker: 64
          gres: 'gpu:1'
          log_directory: ${hydra.job_cwd}/.slurm
          output: slurm-%j.out
          error: slurm-%j.err
    # debug launching issues, set to true to run workers in the same process.
    no_workers: false
```

Running parameter sweeps is easy, just swap run with sweep as the first command:
```text
$ python demos/4_sweep/sweep_example.py sweep
Sweep output dir : /checkpoint/omry/outputs/2019-06-21_20-20-21/
Launching 1 jobs to slurm queue
        Workdir /checkpoint/omry/outputs/2019-06-21_20-20-21/0 :
Dask dashboard for "slurm" at http://localhost:8002.
```

This runs a single job with the default config, but on slurm.