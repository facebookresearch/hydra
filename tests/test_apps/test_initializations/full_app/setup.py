#!/usr/bin/env python

# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from setuptools import find_packages, setup

setup(
    name="test-initialization-app",
    version="0.1",
    packages=find_packages(include=["test_initialization_app"]),
    entry_points={
        "console_scripts": [
            "test-initialization-app = test_initialization_app.main:main"
        ]
    },
    include_package_data=True,
    install_requires=["hydra-core~=1.0.0rc1"],
)
