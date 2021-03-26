# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
# isort: skip_file
from setuptools import find_namespace_packages, setup

import sys
from os.path import abspath, dirname, join

helpers = join(dirname(dirname(dirname(abspath(__file__)))))
sys.path.append(helpers)
from build_helpers.build_helpers import find_version  # noqa E402


with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        name="hydra-nevergrad-sweeper",
        version=find_version(
            dirname(__file__), "hydra_plugins/hydra_nevergrad_sweeper/__init__.py"
        ),
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
            "Programming Language :: Python :: 3.9",
            "Operating System :: OS Independent",
            "Development Status :: 4 - Beta",
        ],
        install_requires=[
            "hydra-core>=1.0.0",
            "nevergrad>=0.4.1.post4",
            "numpy<1.20.0",  # remove once nevergrad is upgraded to support numpy 1.20
        ],
        include_package_data=True,
    )
