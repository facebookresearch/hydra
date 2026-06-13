# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
from pathlib import Path

from read_version import read_version
from setuptools import find_namespace_packages, setup

setup(
    name="hydra-colorlog",
    version=read_version("hydra_plugins/hydra_colorlog", "__init__.py"),
    author="Omry Yadan",
    author_email="omry@fb.com",
    description="Enables colorlog for Hydra apps",
    license="MIT",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/facebookresearch/hydra/",
    packages=find_namespace_packages(include=["hydra_plugins.*"]),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=["colorlog", "hydra-core>=1.0.0"],
    include_package_data=True,
)
