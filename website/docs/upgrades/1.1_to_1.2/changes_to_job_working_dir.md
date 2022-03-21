---
id: changes_to_job_working_dir
title: Changes to job's runtime working directory
hide_title: true
---

Hydra 1.2 introduces `hydra.job.chdir`. This config allows users to specify whether Hydra should change the runtime working
directory to the job's output directory.
`hydra.job.chdir` will default to `False` if version_base is set to >= "1.2" (or None),
or otherwise will use the old behavior and default to `True`, with a warning being issued if `hydra.job.chdir` is not set.

If you want to keep the old Hydra behavior, please set `hydra.job.chdir=True` explicitly for your application.

For more information about `hydra.job.chdir`,
see [Output/Working directory](/tutorials/basic/running_your_app/3_working_directory.md#disable-changing-current-working-dir-to-jobs-output-dir)
and [Job Configuration - hydra.job.chdir](/configure_hydra/job.md#hydrajobchdir).
