# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
from setuptools import find_namespace_packages, setup

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        name="hydra-nevergrad-sweeper",
        version="1.1.0rc1",
        author="Jeremy Rapin, Omry Yadan, Jieru Hu",
        author_email="jrapin@fb.com, omry@fb.com, jieru@fb.com",
        description="Hydra Nevergrad Sweeper plugin",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/facebookresearch/hydra/",
        packages=find_namespace_packages(include=["hydra_plugins.*"]),
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Operating System :: OS Independent",
            "Development Status :: 4 - Beta",
        ],
        install_requires=["hydra-core>=1.0.0", "nevergrad>=0.4.1.post4"],
        include_package_data=True,
    )
