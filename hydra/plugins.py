# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from . import utils


class Plugins:

    @staticmethod
    def _instantiate(config):
        clazz = config['class']
        try:
            if not clazz.startswith(
                    'hydra_plugins.') and not clazz.startswith('hydra.sweeper'):
                # prevent loading plugins in invalid package. this is an indication that it's not a proper plugin
                # and is probably due to pre-plugins config lying around.
                # his also gives us an opportunity confirm that the plugin
                # version is compatible with Hydra's version.
                raise RuntimeError(
                    "Invalid plugin '{}': not in hydra_plugins package, ".format(
                        config['class']))
            plugin = utils.instantiate(config)
        except ImportError as e:
            raise ImportError(
                "Could not instantiate plugin {} : {}\n\n\tIS THE PLUGIN INSTALLED?\n\n".format(
                    config['class'], str(e)))

        return plugin

    @staticmethod
    def instantiate_sweeper(hydra_cfg, config_loader, task_function, verbose):
        cfg = hydra_cfg.hydra.sweeper
        if cfg is None:
            raise RuntimeError("Hydra sweeper is not configured")
        sweeper = Plugins._instantiate(cfg)
        sweeper.setup(
            hydra_cfg=hydra_cfg,
            config_loader=config_loader,
            task_function=task_function,
            verbose=verbose)
        return sweeper

    @staticmethod
    def instantiate_launcher(hydra_cfg, config_loader, task_function, verbose):
        cfg = hydra_cfg.hydra.launcher
        if cfg is None:
            raise RuntimeError("Hydra launcher is not configured")
        launcher = Plugins._instantiate(cfg)
        launcher.setup(config_loader=config_loader,
                       hydra_cfg=hydra_cfg,
                       task_function=task_function,
                       verbose=verbose)
        return launcher
