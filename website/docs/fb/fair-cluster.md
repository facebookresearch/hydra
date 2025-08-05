---
id: fair-cluster
title: Hydra on the FAIR cluster
---

import GithubLink from "@site/src/components/GithubLink"

Hydra 1.0rc is available on FAIR Cluster. The recommended way for installation is via meta package [hydra-fair-plugin](https://github.com/fairinternal/hydra-fair-plugins).

## Hydra FAIR Plugins
1. It brings the correct Hydra dependency and has been tested on the FAIR Cluster.
2. It provides FAIR Cluster specific defaults overrides (for example, ```hydra.sweep.dir``` is set to be ```/checkpoint/${oc.env:USER}/outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}```)
3. It provides a [fairtask](https://github.com/fairinternal/fairtask) launcher plugin.
4. It installs [Submitit](https://github.com/facebookincubator/submitit) launcher plugin by default.

### Installation
<details>
<summary>0.3.1 (stable), compatible with Hydra 0.11</summary>

    ### Clean Install

    ```commandline
    pip install hydra-fair-plugins
    ```

    The dependency installed looks like
    ```commandline
    $ pip freeze | grep hydra
    hydra-core==0.11.3
    hydra-fair-cluster==0.1.4
    hydra-fair-plugins==0.3.1
    hydra-fairtask==0.1.8
    hydra-submitit==0.2.0
    ```
</details>

<details>
    <summary>1.0 (Release candidate), compatible with Hydra 1.0rc</summary>

    With [`Submitit`](https://github.com/facebookincubator/submitit) open sourced, the corresponding plugin has been moved
    <GithubLink to="plugins/hydra_submitit_launcher">here</GithubLink>. Read this [doc](/docs/plugins/submitit_launcher) on installation/usage info.

    ### Clean Install

    ```commandline
    pip install hydra-fair-plugins  --pre --upgrade --upgrade-strategy=eager
    ```

    ### Upgrade from stable

    ```commandline
    # Remove legacy fair internal submitit launcher plugin
    pip uninstall hydra-submitit -y
    pip install hydra-fair-plugins  --pre --upgrade --upgrade-strategy=eager
    ```
    Check out [Hydra documentation](/docs/plugins/submitit_launcher) for  more info on ```Submitit``` launcher plugin.


    The depedency looks like
    ```commandline
    $ pip freeze | grep hydra
    hydra-core==1.0.0rc1
    hydra-fair-cluster==1.0.0rc1
    hydra-fair-plugins==1.0.0rc1
    hydra-fairtask==1.0.0rc1
    hydra-submitit-launcher==1.0.0rc3
    ```

    Please refer to [Hydra upgrades](/docs/upgrades/0.11_to_1.0/config_path_changes) on what changes are needed for your app for upgrading to Hydra 1.0
</details>

<details>
<summary>Downgrade From 1.0rc to stable</summary>

    Downgrade to stable in case you run into issues and need to be unblocked immediately.

    ```commandline
    pip freeze | grep hydra | xargs pip uninstall -y
    pip install hydra-fair-plugins
    ```
</details>

### Usage

<details>
 <summary>0.3.1 (stable)</summary>

    Once the plugins are installed, you can launch to the FAIR cluster by appending hydra/launcher=fairtask or hydra/launcher=submitit
    for example:

    ```
     python my_app.py -m hydra/launcher=submitit db=mysql,postgresql
    # or
     python my_app.py -m hydra/launcher=fairtask db=mysql,postgresql
    ```

    Both hydra-submitit and hydra-fairtask are providing sensible defaults for their configuration ([Submitit](https://github.com/fairinternal/hydra-fair-plugins/blob/master/plugins/hydra-submitit/hydra_plugins/submitit/conf/hydra/launcher/submitit.yaml), [fairtask](https://github.com/fairinternal/hydra-fair-plugins/blob/master/plugins/hydra-fairtask/hydra_plugins/fairtask/conf/hydra/launcher/fairtask.yaml))

    You can customize fairtask/submitit behavior much like you can customize anything else, from the command line or by overriding in your config file or composing in alternative launcher configuration.
    You can view the Hydra config (which includes the config for submitit or fairtask) with this command:
    ```
    python my_app.py hydra/launcher=submitit --cfg=hydra
    ```
</details>


<details>
 <summary>1.0 (Release Candidate)</summary>


    For 1.0, ```fairtask``` usage remains the same. To use ```Submitit```, the command changes to:

    ```commandline
    python my_app.py -m hydra/launcher=submitit_slurm db=mysql,postgresql
    ```

    More info on ```Submitit``` launcher can be found [here](https://hydra.cc/docs/plugins/submitit_launcher)

</details>
