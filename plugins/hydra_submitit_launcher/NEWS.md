1.1.5 (2021-06-10)
==================

### Features

- Add support for SLURM parameters `cpus_per_gpu`, `gpus_per_task`, `mem_per_gpu` and `mem_per_cpu` ([#1366](https://github.com/facebookresearch/hydra/issues/1366))


1.1.5 (2021-06-10)
==================

### Features

- Add support for SLURM parameters `cpus_per_gpu`, `gpus_per_task`, `mem_per_gpu` and `mem_per_cpu` ([#1366](https://github.com/facebookresearch/hydra/issues/1366))


1.1.1 (2021-03-30)
==================

### Maintenance Changes

- Pin Hydra 1.0 plugins to hydra-core==1.0.* to discourage usage with Hydra 1.1 ([#1501](https://github.com/facebookresearch/hydra/issues/1501))


1.1.0 (2021-01-30)
==================

### Features

- Support `additional_parameters` as an optional param in the Submitit launcher plugin. ([#1036](https://github.com/facebookresearch/hydra/issues/1036))
- Support Python 3.9 . ([#1062](https://github.com/facebookresearch/hydra/issues/1062))
- Add support to Submitit's `setup` field for sbatch script [generation](https://github.com/facebookincubator/submitit/blob/2f784bae911cc1ce9112fb742499c5f55e239aa1/submitit/slurm/slurm.py#L387) ([#1227](https://github.com/facebookresearch/hydra/issues/1227))
