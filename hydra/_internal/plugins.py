# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import inspect
import pkgutil
from typing import Any, List, Optional, Type

from omegaconf import DictConfig

from hydra._internal.config.sources_registry import SourcesRegistry
from hydra._internal.config_loader import ConfigLoader
from hydra.types import TaskFunction

from ..plugins import ConfigSource, Launcher, Plugin, Sweeper


class Plugins:
    def __init__(self) -> None:
        raise NotImplementedError("Plugins is a static class, do not instantiate")

    @staticmethod
    def _instantiate(config: DictConfig) -> Plugin:
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
            assert isinstance(plugin, Plugin)

        except ImportError as e:
            raise ImportError(
                "Could not instantiate plugin {} : {}\n\n\tIS THE PLUGIN INSTALLED?\n\n".format(
                    config["class"], str(e)
                )
            )

        return plugin

    @staticmethod
    def is_plugin(clazz: str) -> bool:

        return clazz.startswith("hydra_plugins.") or clazz.startswith(
            "hydra._internal.core_plugins."
        )

    @staticmethod
    def instantiate_sweeper(
        config: DictConfig, config_loader: ConfigLoader, task_function: TaskFunction
    ) -> Sweeper:
        if config.hydra.sweeper is None:
            raise RuntimeError("Hydra sweeper is not configured")
        sweeper = Plugins._instantiate(config.hydra.sweeper)
        assert isinstance(sweeper, Sweeper)
        sweeper.setup(
            config=config, config_loader=config_loader, task_function=task_function
        )
        return sweeper

    @staticmethod
    def instantiate_launcher(
        config: DictConfig, config_loader: ConfigLoader, task_function: TaskFunction
    ) -> Launcher:
        if config.hydra.launcher is None:
            raise RuntimeError("Hydra launcher is not configured")
        launcher = Plugins._instantiate(config.hydra.launcher)
        assert isinstance(launcher, Launcher)
        launcher.setup(
            config=config, config_loader=config_loader, task_function=task_function
        )
        return launcher

    @staticmethod
    def _get_all_subclasses_in(
        modules: List[Any], supertype: Optional[type] = None
    ) -> List[type]:
        """
        :param modules: a list of top level modules to look in
        :param supertype: look for subclasses of this type, if None return all classes
        :return: a set of all classes found
        """
        ret = {}
        for mdl in modules:
            for importer, modname, ispkg in pkgutil.walk_packages(
                path=mdl.__path__, prefix=mdl.__name__ + ".", onerror=lambda x: None
            ):
                loaded_mod = importer.find_module(modname).load_module(modname)
                for name, obj in inspect.getmembers(loaded_mod):
                    if inspect.isclass(obj):
                        if (
                            supertype is None
                            or issubclass(obj, supertype)
                            and not inspect.isabstract(obj)
                        ):
                            ret[obj.__name__] = obj

        return list(ret.values())

    @staticmethod
    def discover(plugin_type: Optional[Type[Plugin]] = None) -> List[Type[Plugin]]:
        """
        :param plugin_type: class of plugin to discover, None for all
        :return: a list of plugins implementing the plugin type (or all if plugin type is None)
        """
        assert plugin_type is None or issubclass(plugin_type, Plugin)
        top_level: List[Any] = []
        from . import core_plugins

        top_level.append(core_plugins)

        try:
            import hydra_plugins

            top_level.append(hydra_plugins)

        except ImportError:
            # If no plugins are installed the hydra_plugins package does not exist.
            pass
        return Plugins._get_all_subclasses_in(top_level, plugin_type)

    @staticmethod
    def register_config_sources() -> None:
        config_sources = Plugins.discover(ConfigSource)
        for source in config_sources:
            assert issubclass(source, ConfigSource)
            SourcesRegistry.instance().register(source)
