# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        name="hydra-fair-cluster-defaults",
        version="0.1.0",
        author="Omry Yadan",
        author_email="omry@fb.com",
        description="Hydra plugin controlling the defaults for the FAIR cluster",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/fairinternal/hydra/",
        packages=find_packages(exclude=["tests"]),
        classifiers=[
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Operating System :: OS Independent",
        ],
        install_requires=[],
        include_package_data=True,
    )
