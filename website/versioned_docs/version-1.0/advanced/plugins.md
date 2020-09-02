---
id: plugins
title: Hydra plugins types
sidebar_label: Hydra plugins
---

Hydra can be extended via plugins.
You can see example plugins [here](https://github.com/facebookresearch/hydra/tree/master/examples/plugins).

<div class="alert alert--info" role="alert">
<strong>NOTE</strong>:
If you develop plugins, please join the <a href="https://hydra-framework.zulipchat.com/#narrow/stream/233935-Hydra-plugin.20dev.20announcements">plugin developer announcement channel</a> in the chat.
</div>
<br/>



## Plugin discovery
The plugin discovery process runs whenever Hydra starts. During plugin discovery, Hydra scans for plugins in all the submodules of `hydra_plugins`. Hydra will import each module and look for plugins defined in that module.
Any module under `hydra_plugins` that is slow to import will slow down the startup of _ALL_ Hydra applicaitons.
Plugins with expensive imports can exclude individual files from this by prefixing them with `_` (but not `__`).
For example, the file `_my_plugin_lib.py` would not be imported and scanned, while `my_plugin_lib.py` would be.

## Plugin types
### Sweeper
A sweeper is responsible for converting command line arguments list into multiple jobs.
For example, the basic built-in sweeper takes arguments like:
```
batch_size=128 optimizer=nesterov,adam learning_rate=0.01,0.1 
```

And creates 4 jobs with the following parameters:
```
batch_size=128 optimizer=nesterov learning_rate=0.01
batch_size=128 optimizer=nesterov learning_rate=0.1
batch_size=128 optimizer=adam learning_rate=0.01
batch_size=128 optimizer=adam learning_rate=0.1
```

### Launcher
Launchers are responsible for launching a job to a specific environment.
A Launcher is taking a batch of argument lists like the one above and launches a job for each one.
The job uses those arguments to compose its configuration.
The basic launcher simply launches the job locally. 

### SearchPathPlugin
A config path plugin can manipulate the search path.
This can be used to influence the default Hydra configuration to be more appropriate to a specific environment,
or just add new entries to the search path to make more configurations available to the Hydra app.

SearchPathPlugin plugins are discovered automatically by Hydra and are being called to manipulate the search path before
the configuration is composed.

Many other plugins also implement SearchPathPlugin to add their configuration to the config search path once they are installed. 

### ConfigSource
ConfigSource plugins can be used to allow Hydra to access configuration in non-standard locations when composing the config.
This can be used to enable to access an in-house private config store, or as a way to access configs from public sources like GitHub or S3.
