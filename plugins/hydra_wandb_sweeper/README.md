## WandB sweeper integration with Hydra

### Installing

```bash
$ pip install git+https://github.com/captain-pool/hydra-wandb-sweeper.git
```


## Usage

Using this plugin is very simple, as one can just invoke the sweeper by overriding `hydra/sweeper` with `wandb`.

```python
@hydra.main(config_path=..., config_name=...)
def main(cfg: DictConfig):

  with wandb.init(id=run_id) as run:
    ...
    wandb.log({"loss": loss})
```


## Hydra Overrides

### Passing Distributions for continuous parameters

Sweeping over continuous params (for ex. learning rates in ML pipelines) can be done by passing the upper limit and lower with the hydra's `interval(<min>, <max>)` override. For example:
```
$ python3 /path/to/trainer/file hydra/sweeper=wandb model.learning_rate="interval(0.1, 0.2)"
```

By default, the `interval()` sweep uses the uniform distribution while making parameter suggestions. To use a different distribution add the name of the supported distribution (`uniform`, `log_uniform`, `q_uniform`, `q_log_uniform`, `q_normal`, `log_normal`, `q_log_normal`) as a [`tag`](https://hydra.cc/docs/advanced/override_grammar/extended/#tag) to the [`interval()`](https://hydra.cc/docs/advanced/override_grammar/extended/#interval-sweep) sweep. For example, to use a normal distribution with `mean=0` and `variance=1` to suggest a value for `learning_rate` use the following:
```
$ python3 /path/to/trainer/file hydra/sweeper=wandb model.learning_rate="tag(normal, interval(0, 1))"
```

### Categorial parameters

Sweeping over categorical items is as simple as passing a list of items to sweep over thereby directly using Hydra' [`choice()`](https://hydra.cc/docs/advanced/override_grammar/extended/#choice-sweep) sweep feature. for example, to sweep over a categorical list of `batch_size`,
```
$ python3 /path/to/trainer/file hydra/sweeper=wandb model.batch_size=8,10,12,14
```
Equivalently, the `choice()` command can also be expliclty used:
```
$python3 /path/to/trainer/file hydra/sweep=wandb model.batch_size="choice(8,10,12,14)".
```


Categorical sweep can also be done using hydra's [`range()`](https://hydra.cc/docs/advanced/override_grammar/extended/#range-sweep) sweep. The previous task can be equivalently achieved as:
```
$ python3 /path/to/trainer/file hydra/sweeper=wandb model.batch_size="range(8, 15, step=2)"
```
