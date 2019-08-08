# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        name="hydra-submitit",
        version="0.1.0",
        author="Omry Yadan",
        author_email="omry@fb.com",
        description="Submitit plugin for Hydra",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/fairinternal/hydra",
        packages=find_packages(exclude=['tests']),
        classifiers=[
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            'submitit@git+ssh://git@github.com/fairinternal/submitit.git@master',
        ],
    )
