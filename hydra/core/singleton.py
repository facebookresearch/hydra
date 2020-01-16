# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any, Dict


class Singleton(type):
    _instances: Dict[type, "Singleton"] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def instance(cls: Any, *args: Any, **kwargs: Any) -> Any:
        return cls(*args, **kwargs)

    @staticmethod
    def get_state() -> Dict[type, "Singleton"]:
        return Singleton._instances

    @staticmethod
    def set_state(instances: Dict[type, "Singleton"]) -> None:
        Singleton._instances = instances
