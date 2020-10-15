# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from setuptools import find_namespace_packages, setup

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        name="hydra-ray-launcher",
        version="0.1.0",
        author="Jieru Hu",
        author_email="jieru@fb.com",
        description="Hydra Ray launcher plugin",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/facebookresearch/hydra/",
        packages=find_namespace_packages(include=["hydra_plugins.*"]),
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Operating System :: MacOS",
            "Operating System :: POSIX :: Linux",
        ],
        install_requires=[
            "boto3==1.15.6",
            "hydra-core>=1.0.0",
            "ray>=1.0.0",
            "cloudpickle>=1.6.0",
            "pickle5",
        ],
        include_package_data=True,
    )
