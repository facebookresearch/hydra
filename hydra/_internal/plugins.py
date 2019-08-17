# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved


class Plugins:
    @staticmethod
    def _instantiate(config):
        clazz = config["class"]
        try:
            if clazz is None:
                raise ImportError("class not configured")

            if not Plugins.is_plugin(clazz):
                # prevent loading plugins in invalid package. this is an indication that it's not
                # a proper plugin and is probably due to pre-plugins config lying around.
                # his also gives us an opportunity confirm that the plugin
                # version is compatible with Hydra's version.
                raise RuntimeError(
                    "Invalid plugin '{}': not in hydra_plugins package, ".format(
                        config["class"]
                    )
                )
            from ..utils import instantiate

            plugin = instantiate(config)
        except ImportError as e:
            raise ImportError(
                "Could not instantiate plugin {} : {}\n\n\tIS THE PLUGIN INSTALLED?\n\n".format(
                    config["class"], str(e)
                )
            )

        return plugin

    @staticmethod
    def is_plugin(clazz):

        return clazz.startswith("hydra_plugins.") or clazz.startswith(
            "hydra._internal.core_plugins."
        )

    @staticmethod
    def instantiate_sweeper(config, config_loader, task_function, verbose):
        if config.hydra.sweeper is None:
            raise RuntimeError("Hydra sweeper is not configured")
        sweeper = Plugins._instantiate(config.hydra.sweeper)
        sweeper.setup(
            config=config,
            config_loader=config_loader,
            task_function=task_function,
            verbose=verbose,
        )
        return sweeper

    @staticmethod
    def instantiate_launcher(config, config_loader, task_function, verbose):
        if config.hydra.launcher is None:
            raise RuntimeError("Hydra launcher is not configured")
        launcher = Plugins._instantiate(config.hydra.launcher)
        launcher.setup(
            config=config,
            config_loader=config_loader,
            task_function=task_function,
            verbose=verbose,
        )
        return launcher
