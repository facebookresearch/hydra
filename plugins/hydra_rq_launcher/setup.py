# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
from setuptools import find_namespace_packages, setup

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        name="hydra-rq-launcher",
        version="1.0.2",
        author="Jan-Matthis Lueckmann, Omry Yadan",
        author_email="mail@jan-matthis.de, omry@fb.com",
        description="Redis Queue (RQ) Launcher for Hydra apps",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/facebookresearch/hydra/",
        packages=find_namespace_packages(include=["hydra_plugins.*"]),
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Operating System :: MacOS",
            "Operating System :: POSIX :: Linux",
        ],
        install_requires=[
            "cloudpickle",
            "fakeredis",
            "hydra-core>=1.0.0",
            "rq>=1.5.1",
        ],
        include_package_data=True,
    )
