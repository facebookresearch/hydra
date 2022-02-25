## WandB sweeper integration with Hydra

### Installing

```bash
$ pip install git+https://github.com/captain-pool/hydra-wandb-sweeper.git
```


## Usage

Using this plugin is very simple, as one can just invoke the sweeper by overriding `hydra/sweeper` with `wandb`.

The only difference this plugin has with respect to other regular hydra plugin, is the function signature of `main` requires the presence of an additional positional argument called `run_id`.

Hence, the final function would something like:
```python
@hydra.main(config_path=..., config_name=...)
def main(cfg: DictConfig, run_id: str): # notice the extra run_id parameter

  with wandb.init(id=run_id) as run:
    ...
    wandb.log({"loss": loss})
```

To make the main support other launchers as well, an user can mark the `run_id` parameter optional like the following:

```python
@hydra.main(config_path=..., config_name=...)
def main(cfg: DictConfig, run_id: Optional[str] = None):

with wandb.init(id=run_id) as run:
  ...
  wandb.log({"loss": loss})
```
