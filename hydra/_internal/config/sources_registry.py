# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any, Dict, Type

from ..singleton import Singleton
from .config_source import ConfigSource


class SourcesRegistry(metaclass=Singleton):
    types: Dict[str, Type[ConfigSource]]

    def __init__(self) -> None:
        self.types = {}

    def register(self, schema: str, type_: Type[ConfigSource]) -> None:
        assert (
            schema not in self.types or self.types[schema] is type_
        ), f"{schema} is already registered with a different class"
        self.types[schema] = type_

    def resolve(self, schema: str) -> Type[ConfigSource]:
        if schema not in self.types:
            raise ValueError(f"No config source registered for schema {schema}")
        return self.types[schema]

    @staticmethod
    def instance(*args: Any, **kwargs: Any) -> "SourcesRegistry":
        return Singleton.instance(SourcesRegistry, *args, **kwargs)  # type: ignore
