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
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/facebookresearch/hydra/",
    packages=find_namespace_packages(include=["hydra_plugins.*"]),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        # "Programming Language :: Python :: 3.9",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
        "boto3==1.17.17",
        "hydra-core>=1.1.0.dev7",
        "ray==1.3.0",
        "cloudpickle==1.6.0",
        "pickle5==0.0.11",
    ],
    include_package_data=True,
)
