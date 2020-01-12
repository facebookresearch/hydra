# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        name="hydra-ax-sweeper",
        version="0.1.0",
        author="Omry Yadan, Shagun Sodhani",
        author_email="omry@fb.com, sshagunsodhani@gmail.com",
        description="Hydra Ax Sweeper plugin",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/facebookresearch/hydra/",
        packages=find_packages(exclude=["tests", "example"]),
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            "hydra-core",
            "botorch==0.1.3",
            "sqlalchemy",
            "ax-platform==0.1.6",
        ],
        include_package_data=True,
    )
