# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from .config_repository import ConfigRepository
from .config_source import ConfigSource, ObjectType
from .file_config_source import FileConfigSource
from .package_config_source import PackageConfigSource
from .sources_registry import SourcesRegistry

# Register built in schema types
SourcesRegistry.instance().register("file", FileConfigSource)
SourcesRegistry.instance().register("pkg", PackageConfigSource)


__all__ = [
    "SourcesRegistry",
    "PackageConfigSource",
    "FileConfigSource",
    "ConfigSource",
    "ConfigRepository",
    "ObjectType",
]
