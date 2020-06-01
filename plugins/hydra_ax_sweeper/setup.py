# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
from setuptools import find_namespace_packages, setup

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        name="hydra-ax-sweeper",
        version="1.0.0rc4",
        author="Omry Yadan, Shagun Sodhani",
        author_email="omry@fb.com, sshagunsodhani@gmail.com",
        description="Hydra Ax Sweeper plugin",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/facebookresearch/hydra/",
        packages=find_namespace_packages(include=["hydra_plugins.*"]),
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Operating System :: POSIX :: Linux",
            "Development Status :: 4 - Beta",
        ],
        install_requires=["hydra-core~=1.0.0rc1", "ax-platform[mysql]==0.1.9"],
        include_package_data=True,
    )
