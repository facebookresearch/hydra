# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
from pathlib import Path

from read_version import read_version
from setuptools import find_namespace_packages, setup

setup(
    name="hydra-nevergrad-sweeper",
    version=read_version("hydra_plugins/hydra_nevergrad_sweeper", "__init__.py"),
    author="Jeremy Rapin, Omry Yadan, Jieru Hu",
    author_email="jrapin@fb.com, omry@fb.com, jieru@fb.com",
    description="Hydra Nevergrad Sweeper plugin",
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
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.10",
    install_requires=[
        "hydra-core>=1.1.0.dev7",
        "nevergrad>=0.4.3.post9",
    ],
    include_package_data=True,
)
