# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import importlib
import inspect
import pkgutil
import warnings
from collections import defaultdict
from dataclasses import dataclass
from timeit import default_timer as timer
from typing import Any, Dict, List, Optional, Type

from omegaconf import DictConfig

from hydra._internal.sources_registry import SourcesRegistry
from hydra.conf import PluginConf
from hydra.core.config_loader import ConfigLoader
from hydra.core.singleton import Singleton
from hydra.plugins.completion_plugin import CompletionPlugin
from hydra.plugins.config_source import ConfigSource
from hydra.plugins.launcher import Launcher
from hydra.plugins.plugin import Plugin
from hydra.plugins.search_path_plugin import SearchPathPlugin
from hydra.plugins.sweeper import Sweeper
from hydra.types import TaskFunction


@dataclass
class PluginMetadata:
    cls: Type[Plugin]
    import_time: float


class Plugins(metaclass=Singleton):
    @staticmethod
    def instance(*args: Any, **kwargs: Any) -> "Plugins":
        ret = Singleton.instance(Plugins, *args, **kwargs)
        assert isinstance(ret, Plugins)
        return ret

    def __init__(self) -> None:
        self.plugin_type_to_subclass_list: Dict[Type[Plugin], List[PluginMetadata]] = {}
        self.class_name_to_class: Dict[str, Type[Plugin]] = {}
        self.initialize()

    def initialize(self) -> None:
        top_level: List[Any] = []
        core_plugins = importlib.import_module("hydra._internal.core_plugins")
        top_level.append(core_plugins)

        try:
            hydra_plugins = importlib.import_module("hydra_plugins")
            top_level.append(hydra_plugins)
        except ImportError:
            # If no plugins are installed the hydra_plugins package does not exist.
            pass
        self.plugin_type_to_subclass_list = self._scan_all_plugins(modules=top_level)
        self.class_name_to_class = {}
        for plugin_type, plugin_metas in self.plugin_type_to_subclass_list.items():
            for pm in plugin_metas:
                clazz = pm.cls
                name = f"{clazz.__module__}.{clazz.__name__}"
                self.class_name_to_class[name] = clazz

        # Register config sources
        for source in self.plugin_type_to_subclass_list[ConfigSource]:
            assert issubclass(source.cls, ConfigSource)
            SourcesRegistry.instance().register(source.cls)

    def _instantiate(self, config: PluginConf) -> Plugin:
        import hydra.utils as utils

        classname = utils._get_class_name(config)
        try:
            if classname is None:
                raise ImportError("class not configured")

            if not self.is_in_toplevel_plugins_module(classname):
                # All plugins must be defined inside the approved top level modules.
                # For plugins outside of hydra-core, the approved module is hydra_plugins.
                raise RuntimeError(
                    f"Invalid plugin '{classname}': not the hydra_plugins package"
                )

            if classname not in self.class_name_to_class.keys():
                raise RuntimeError(f"Unknown plugin class : '{classname}'")
            clazz = self.class_name_to_class[classname]
            plugin = utils._instantiate_class(clazz=clazz, config=config)
            assert isinstance(plugin, Plugin)

        except ImportError as e:
            raise ImportError(
                "Could not instantiate plugin {} : {}\n\n\tIS THE PLUGIN INSTALLED?\n\n".format(
                    config["class"], str(e)
                )
            )

        return plugin

    def is_in_toplevel_plugins_module(self, clazz: str) -> bool:

        return clazz.startswith("hydra_plugins.") or clazz.startswith(
            "hydra._internal.core_plugins."
        )

    def instantiate_sweeper(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> Sweeper:
        Plugins.check_usage(self)
        if config.hydra.sweeper is None:
            raise RuntimeError("Hydra sweeper is not configured")
        sweeper = self._instantiate(config.hydra.sweeper)
        assert isinstance(sweeper, Sweeper)
        sweeper.setup(
            config=config, config_loader=config_loader, task_function=task_function
        )
        return sweeper

    def instantiate_launcher(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> Launcher:
        Plugins.check_usage(self)
        if config.hydra.launcher is None:
            raise RuntimeError("Hydra launcher is not configured")
        launcher = self._instantiate(config.hydra.launcher)
        assert isinstance(launcher, Launcher)
        launcher.setup(
            config=config, config_loader=config_loader, task_function=task_function
        )
        return launcher

    def _scan_all_plugins(
        self, modules: List[Any]
    ) -> Dict[Type[Plugin], List[PluginMetadata]]:
        ret: Dict[Type[Plugin], List[PluginMetadata]] = defaultdict(list)

        plugin_types = [
            Plugin,
            ConfigSource,
            CompletionPlugin,
            Launcher,
            Sweeper,
            SearchPathPlugin,
        ]

        for mdl in modules:
            for importer, modname, ispkg in pkgutil.walk_packages(
                path=mdl.__path__, prefix=mdl.__name__ + ".", onerror=lambda x: None
            ):
                try:
                    start = timer()
                    m = importer.find_module(modname)
                    loaded_mod = m.load_module(modname)
                    import_time = timer() - start

                    if loaded_mod is not None:
                        for name, obj in inspect.getmembers(loaded_mod):
                            if (
                                inspect.isclass(obj)
                                and issubclass(obj, Plugin)
                                and not inspect.isabstract(obj)
                            ):
                                for plugin_type in plugin_types:
                                    if issubclass(obj, plugin_type):
                                        pm = PluginMetadata(
                                            cls=obj, import_time=import_time
                                        )
                                        ret[plugin_type].append(pm)
                except ImportError as e:
                    warnings.warn(
                        message=f"\n"
                        f"\tError importing '{modname}'.\n"
                        f"\tPlugin is incompatible with this Hydra version or buggy.\n"
                        f"\tRecommended to uninstall or upgrade plugin.\n"
                        f"\t\t{type(e).__name__} : {e}",
                        category=UserWarning,
                    )
        return ret

    def discover(
        self, plugin_type: Optional[Type[Plugin]] = None
    ) -> List[Type[Plugin]]:
        """
        :param plugin_type: class of plugin to discover, None for all
        :return: a list of plugins implementing the plugin type (or all if plugin type is None)
        """
        Plugins.check_usage(self)
        ret: List[Type[Plugin]] = []
        if plugin_type is None:
            plugin_type = Plugin
        assert issubclass(plugin_type, Plugin)
        if plugin_type not in self.plugin_type_to_subclass_list:
            return []
        for pm in self.plugin_type_to_subclass_list[plugin_type]:
            ret.append(pm.cls)

        return ret

    @staticmethod
    def check_usage(self_: Any) -> None:
        if not isinstance(self_, Plugins):
            raise ValueError(
                f"Plugins is now a Singleton. usage: Plugins.instance().{inspect.stack()[1][3]}(...)"
            )
