# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        name="hydra-colorlog",
        version="0.1.4",
        author="Omry Yadan",
        author_email="omry@fb.com",
        description="Enables colorlog for Hydra apps",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/facebookresearch/hydra/",
        packages=find_packages(exclude=["tests"]),
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Operating System :: OS Independent",
        ],
        install_requires=["colorlog", "hydra-core"],
        include_package_data=True,
    )
