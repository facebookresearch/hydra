# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
from pathlib import Path

from read_version import read_version
from setuptools import find_namespace_packages, setup

setup(
    name="hydra-ax-sweeper",
    version=read_version("hydra_plugins/hydra_ax_sweeper", "__init__.py"),
    author="Omry Yadan, Shagun Sodhani",
    author_email="omry@fb.com, sshagunsodhani@gmail.com",
    description="Hydra Ax Sweeper plugin",
    license="MIT",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/facebookresearch/hydra/",
    packages=find_namespace_packages(include=["hydra_plugins.*"]),
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.11,<3.15",
    install_requires=[
        "hydra-core>=1.1.0.dev7",
        "ax-platform>=1.2.4,<1.3.0",
        "torch>=2.2",
    ],
    include_package_data=True,
)
