---
id: changes_to_sweeper_config
title: Changes to configuring sweeper's search space
hide_title: true
---

Hydra 1.2 introduces `hydra.sweeper.params`. All Hydra Sweepers (BasicSweeper and HPOs) search
space will be defined under this config node.


### Optuna 
For migration, move search space definition from `hydra.sweeper.search_space` to `hydra.sweeper.params`. Change the search space
definition to be consistent with how you'd override a value from commandline. For example:

<div className="row">
<div className="col col--6">

```yaml title="Hydra 1.1"
hydra:
  sweeper:
    search_space:
      search_space:
        x:
          type: float
          low: -5.5
          high: 5.5
          step: 0.5
        'y':
          type: categorical
          choices:
          - -5
          - 0
          - 5
```
</div>
<div className="col  col--6">

```bash title="Hydra 1.2"
hydra:
  sweeper:
    params:
      x: range(-5.5, 5.5, step=0.5)
      y: choice(-5, 0, 5)










```
</div>
</div>

Check out [Optuna Sweeper](/plugins/optuna_sweeper.md) for more info.

### Nevergrad 
Search space definition is moved from `hydra.sweeper.parametrization` to `hydra.sweeper.params`. 
Change the search space definition to be consistent with how you'd override a value from commandline. 
Nevergrad's Scalar supports a few unique way of defining `Scalar` (for example, a log scaled interval without upper bound).
In this case, you can pass in your paremeters as a dict. 

For example:

<div className="row">
<div className="col col--6">

```yaml title="Hydra 1.1"
hydra:
  sweeper:
    parametrization:
      db:
        - mnist
        - cifar
      lr:
        init: 0.02
        step: 2.0
        log: true
      dropout:
        lower: 0.0
        upper: 1.0
      batch_size:
        lower: 4
        upper: 16
        integer: true
```
</div>
<div className="col  col--6">

```bash title="Hydra 1.2"
hydra:
  sweeper:
    params:
      db: choice(mnist, cifar)
      lr: {init: 0.02,step: 2.0,log: true}
      dropout: interval(0, 1)
      batch_size: range(4, 16)










```
</div>
</div>

Check out [Nevergrad Sweeper](/plugins/nevergrad_sweeper.md) for more info.