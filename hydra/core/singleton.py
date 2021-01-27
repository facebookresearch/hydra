# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from copy import deepcopy
from typing import Any, Dict

from omegaconf.basecontainer import BaseContainer


class Singleton(type):
    _instances: Dict[type, "Singleton"] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def instance(cls: Any, *args: Any, **kwargs: Any) -> Any:
        return cls(*args, **kwargs)

    @staticmethod
    def get_state() -> Any:
        instances = deepcopy(Singleton._instances)
        # Plugins can cause issues when unpickling the singleton state
        # if not all plugins are available on the the side doing the unpickling.
        # Exclude them and re-initialize them on set_state()
        from hydra.core.plugins import Plugins

        instances.pop(Plugins, None)
        return {
            "instances": instances,
            "omegaconf_resolvers": deepcopy(BaseContainer._resolvers),
        }

    @staticmethod
    def set_state(state: Any) -> None:
        Singleton._instances = state["instances"]
        # Reinitialize the the Plugin singleton (re-discover plugins).
        from hydra.core.plugins import Plugins

        Plugins.instance()
        BaseContainer._resolvers = deepcopy(state["omegaconf_resolvers"])
