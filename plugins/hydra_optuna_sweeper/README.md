# Hydra Optuna Sweeper

Provides an [Optuna](https://optuna.org) based Hydra Sweeper.

See [website](https://hydra.cc/docs/plugins/optuna_sweeper/) for more information.

## Updates

If you want to use the GPSampler, you need to suppress the warnings from Optuna. You can do this by adding the following code to your script:

```python
import warnings
from optuna.exceptions import ExperimentalWarning

warnings.filterwarnings("ignore", category=ExperimentalWarning)
```
