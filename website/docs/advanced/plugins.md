---
id: plugins
title: Hydra plugins
sidebar_label: Hydra plugins
---

Hydra has a plugin architecture.
Plugin types includes:

## Sweeper
A sweeper is responsible for convert a command line into multiple jobs.
For example, the basic built-in sweeper takes arguments like:
```
hydra/launcher=fairtask optimizer=nesterov,adam learning_rate=0.01,0.1 
```

And launches 4 jobs with the following parameters:
```
hydra/launcher=fairtask optimizer=nesterov learning_rate=0.01
hydra/launcher=fairtask optimizer=nesterov learning_rate=0.1
hydra/launcher=fairtask optimizer=adam learning_rate=0.01
hydra/launcher=fairtask optimizer=adam learning_rate=0.1
```


## Launcher
A launcher is taking a batch of argument lists like the one above and launches a job for each one.
The job uses those arguments to compose a it's configuration.
The basic launcher simply launches the job locally 

## SearchPathPlugin
A config path plugin can manipulate the search path.
This can be used to influence the default Hydra configuration to be more appropriate to a specific environment,
or just add new entries to the search path to make more configurations available to the Hydra app.

SearchPathPlugin plugins are discovered automatically by Hydra and are being called to manipulate the search path before
the configuration is composed.