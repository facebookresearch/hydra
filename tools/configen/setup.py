#!/usr/bin/env python

# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from setuptools import find_packages, setup

setup(
    name="neoconfigen",
    version="1.0.0",
    packages=find_packages(include=["configen"]),
    entry_points={"console_scripts": ["configen = configen.configen:main"]},
    author="Omry Yadan, Rosario Scalise",
    author_email="omry@fb.com, rosario@cs.uw.edu",
    url="https://github.com/predictive-analytics-lab/neoconfigen",
    include_package_data=True,
    install_requires=["hydra-core>=1.1.0dev1", "jinja2"],
)
