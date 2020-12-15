#!/usr/bin/env python

# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from setuptools import find_packages, setup

setup(
    name="initialization-test-app",
    version="0.1",
    packages=find_packages(include=["initialization_test_app"]),
    entry_points={
        "console_scripts": [
            "initialization-test-app = initialization_test_app.main:main"
        ]
    },
    include_package_data=True,
    install_requires=["hydra-core"],
)
