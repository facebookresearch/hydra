# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
from pathlib import Path

from read_version import read_version
from setuptools import find_namespace_packages, setup

setup(
    name="hydra-orion-sweeper",
    version=read_version("hydra_plugins/hydra_orion_sweeper", "__init__.py"),
    author="Pierre Delaunay",
    author_email="pierre.delaunay@mila.quebec",
    description="Hydra Orion Sweeper plugin",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://orion.readthedocs.io/",
    packages=find_namespace_packages(include=["hydra_plugins.*"]),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    install_requires=[
        "hydra-core>=1.1.0.dev7",
        "orion>=0.2.2",
    ],
    include_package_data=True,
)
