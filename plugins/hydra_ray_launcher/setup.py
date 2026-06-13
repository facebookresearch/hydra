# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
from pathlib import Path

from read_version import read_version
from setuptools import find_namespace_packages, setup

setup(
    name="hydra-ray-launcher",
    version=read_version("hydra_plugins/hydra_ray_launcher", "__init__.py"),
    author="Jieru Hu",
    author_email="jieru@fb.com",
    description="Hydra Ray launcher plugin",
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
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.10",
    install_requires=[
        "boto3",
        "hydra-core>=1.1.2",
        "ray[default]<3",
        "aiohttp<4",
        "cloudpickle<3",
    ],
    include_package_data=True,
)
