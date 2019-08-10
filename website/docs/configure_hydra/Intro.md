---
id: intro
title: Configuring  Hydra
sidebar_label: Introduction
---

Hydra comes pre-packages with sensible default configuration that covers the basic use cases.
You can customize that behavior by creating a `.hydra/hydra.yaml` file under your job config path.

### Working directories
Job output directory can be [customized](workdir) both for local and for cluster (sweep) runs.

### Logging
The default logging should be sufficient for most use cases but you can [customize](logging) 
the logging in your own project 

### Task name
By default, the task name is simply the name of the python file without the .py extension.
In some cases you may want to [customize](task_name) it.

### Plugins
Many plugins requires configuration via the .hydra directory.
See the documentation of individual plugins for more information about how to configure them.

