# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
from pathlib import Path

from read_version import read_version
from setuptools import find_namespace_packages, setup

setup(
    name="hydra-rq-launcher",
    version=read_version("hydra_plugins/hydra_rq_launcher", "__init__.py"),
    author="Jan-Matthis Lueckmann, Omry Yadan",
    author_email="mail@jan-matthis.de, omry@fb.com",
    description="Redis Queue (RQ) Launcher for Hydra apps",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/facebookresearch/hydra/",
    packages=find_namespace_packages(include=["hydra_plugins.*"]),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
        "cloudpickle",
        "fakeredis",
        "hydra-core>=1.1.0.dev7",
        "rq>=1.5.1",
    ],
    include_package_data=True,
)
