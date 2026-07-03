Support the latest version of Optuna
The `consider_prior`, `prior_weight`, `consider_magic_clip`, `consider_endpoints`, and `warn_independent_sampling` options of the TPE sampler config remain available but are deprecated in Optuna 4.x; Optuna emits a deprecation warning when they are used
Removed MOTPESampler support, as it has been removed in Optuna v4.0.0
Added GPSampler support for Gaussian Process based optimization ([Optuna GPSampler](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.GPSampler.html))
Added QMCSampler support for Quasi Monte Carlo based optimization ([Optuna QMCSampler](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.QMCSampler.html))
