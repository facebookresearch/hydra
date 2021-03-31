## Release tool.

A few usage examples:

Check all plugins against the published versions:
```text
$ python tools/release/release.py  action=check set=plugins 
[2021-03-30 18:21:05,768][__main__][INFO] - Build outputs : /home/omry/dev/hydra/outputs/2021-03-30/18-21-05/build
[2021-03-30 18:21:05,768][__main__][INFO] - Checking for unpublished packages
[2021-03-30 18:21:06,258][__main__][INFO] - ❋ : hydra-ax-sweeper : newer (local=1.1.5.dev1 > latest=1.1.0rc2)
[2021-03-30 18:21:06,746][__main__][INFO] - ❋ : hydra-colorlog : newer (local=1.1.0.dev1 > latest=1.0.1)
[2021-03-30 18:21:07,232][__main__][INFO] - ❋ : hydra-joblib-launcher : newer (local=1.1.5.dev1 > latest=1.1.2)
[2021-03-30 18:21:07,708][__main__][INFO] - ❋ : hydra-nevergrad-sweeper : newer (local=1.1.5.dev1 > latest=1.1.0rc2)
[2021-03-30 18:21:08,161][__main__][INFO] - ❋ : hydra-optuna-sweeper : newer (local=1.1.0.dev1 > latest=0.9.0rc2)
[2021-03-30 18:21:08,639][__main__][INFO] - ❋ : hydra-ray-launcher : newer (local=1.1.0.dev1 > latest=0.1.4)
[2021-03-30 18:21:09,122][__main__][INFO] - ❋ : hydra-rq-launcher : newer (local=1.1.0.dev1 > latest=1.0.2)
[2021-03-30 18:21:09,620][__main__][INFO] - ❋ : hydra-submitit-launcher : newer (local=1.1.5.dev1 > latest=1.1.1)
```

Check specific packages (hydra and configen) against the published versions
```text
$ python tools/release/release.py  action=check packages=[hydra,configen]
[2021-03-30 18:21:25,423][__main__][INFO] - Build outputs : /home/omry/dev/hydra/outputs/2021-03-30/18-21-25/build
[2021-03-30 18:21:25,423][__main__][INFO] - Checking for unpublished packages
[2021-03-30 18:21:26,042][__main__][INFO] - ❋ : hydra-core : newer (local=1.1.0.dev6 > latest=1.1.0.dev5)
[2021-03-30 18:21:26,497][__main__][INFO] - ❋ : hydra-configen : newer (local=0.9.0.dev8 > latest=0.9.0.dev7)
```

Build all plugins:
```shell
$ python tools/release/release.py  action=build set=plugins
[2021-03-30 18:21:40,426][__main__][INFO] - Build outputs : /home/omry/dev/hydra/outputs/2021-03-30/18-21-40/build
[2021-03-30 18:21:40,426][__main__][INFO] - Building unpublished packages
[2021-03-30 18:21:41,280][__main__][INFO] - Building hydra-ax-sweeper
[2021-03-30 18:21:47,237][__main__][INFO] - Building hydra-colorlog
[2021-03-30 18:21:52,982][__main__][INFO] - Building hydra-joblib-launcher
[2021-03-30 18:21:58,833][__main__][INFO] - Building hydra-nevergrad-sweeper
[2021-03-30 18:22:04,618][__main__][INFO] - Building hydra-optuna-sweeper
[2021-03-30 18:22:10,511][__main__][INFO] - Building hydra-ray-launcher
[2021-03-30 18:22:16,487][__main__][INFO] - Building hydra-rq-launcher
[2021-03-30 18:22:22,302][__main__][INFO] - Building hydra-submitit-launcher
```

Publish all build articats (sdists and wheels):
```
$ twine upload /home/omry/dev/hydra/outputs/2021-03-30/18-21-40/build/*
...
```
