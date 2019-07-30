from . import utils


class Plugins:

    @staticmethod
    def _instantiate(cfg):
        try:
            plugin = utils.instantiate_plugin(cfg)
        except ImportError as e:
            raise ImportError(
                "Could not instantiate plugin {} : {}\n\n\tIS THE PLUGIN INSTALLED?\n\n".format(
                    cfg['class'], str(e)
                ))

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
