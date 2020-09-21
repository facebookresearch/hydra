#!/usr/bin/env python

# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from setuptools import find_packages, setup

setup(
    name="hydra-configen",
    version="0.9.0dev5",
    packages=find_packages(include=["configen"]),
    entry_points={"console_scripts": ["configen = configen.configen:main"]},
    author="Omry Yadan",
    author_email="omry@fb.com",
    url="http://hydra.cc",
    include_package_data=True,
    install_requires=["hydra-core>=1.0.0", "jinja2"],
)
