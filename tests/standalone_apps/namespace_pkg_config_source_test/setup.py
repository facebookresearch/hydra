# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from setuptools import find_namespace_packages, setup

setup(
    name="hydra-namespace-test-app",
    version="0.1.0",
    author="Omry Yadan",
    author_email="omry@fb.com",
    url="https://github.com/facebookresearch/hydra/",
    packages=find_namespace_packages(include=["some_namespace.*"]),
    install_requires=["hydra-core"],
)
