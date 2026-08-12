---
id: changes_to_job_working_dir
title: Changes to job's runtime working directory
hide_title: true
---

Hydra 1.2 introduced `hydra.job.chdir`. This config controls whether Hydra changes
the runtime working directory to the job's output directory. The current default
is `False`.

If you want to keep the old Hydra behavior, please set `hydra.job.chdir=True` explicitly for your application.

For more information about `hydra.job.chdir`,
see [Output/Working directory](/tutorials/basic/running_your_app/3_working_directory.md#automatically-change-current-working-dir-to-jobs-output-dir)
and [Job Configuration - hydra.job.chdir](/configure_hydra/job.md#hydrajobchdir).
