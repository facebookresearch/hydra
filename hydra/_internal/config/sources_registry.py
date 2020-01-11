# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any, Dict, Type

from hydra.plugins.config_source import ConfigSource

from ..singleton import Singleton


class SourcesRegistry(metaclass=Singleton):
    types: Dict[str, Type[ConfigSource]]

    def __init__(self) -> None:
        self.types = {}

    def register(self, type_: Type[ConfigSource]) -> None:
        schema = type_.schema()
        if schema in self.types:
            if self.types[schema].__name__ != type_.__name__:
                raise ValueError(
                    f"{schema} is already registered with a different class"
                )
            else:
                # Do not replace existing ConfigSource
                return
        self.types[schema] = type_

    def resolve(self, schema: str) -> Type[ConfigSource]:
        if schema not in self.types:
            raise ValueError(f"No config source registered for schema {schema}")
        return self.types[schema]

    @staticmethod
    def instance(*args: Any, **kwargs: Any) -> "SourcesRegistry":
        return Singleton.instance(SourcesRegistry, *args, **kwargs)  # type: ignore
