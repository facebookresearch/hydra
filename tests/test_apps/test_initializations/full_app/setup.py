#!/usr/bin/env python

# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from setuptools import setup

setup(
    name="test-initialization-app",
    version="0.1",
    packages=["hydra_app"],
    entry_points={"console_scripts": ["test-initialization-app = hydra_app.main:main"]},
    author="you!",
    author_email="your_email@example.com",
    url="http://hydra-app.example.com",
    include_package_data=True,
    install_requires=["hydra-core~=1.0.0rc1"],
)
