# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from setuptools import find_namespace_packages, setup

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        name="hydra-submitit-launcher",
        version="1.0.0rc1",
        author="Omry Yadan, Jieru Hu",
        author_email="omry@fb.com, jieru@fb.com",
        description="Submitit Launcher for Hydra apps",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/facebookincubator/submitit",
        packages=find_namespace_packages(include=["hydra_plugins.*"]),
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Operating System :: MacOS",
            "Operating System :: POSIX :: Linux",
            "Development Status :: 4 - Beta",
        ],
        install_requires=["hydra-core~=1.0.0rc1", "submitit>=1.0.0"],
        include_package_data=True,
    )
