`hydra.utils.instantiate()` calls on OmegaConf inputs without call-site
overrides no longer make an additional full-tree copy. Benchmarked calls run 4
to 10 times faster.
