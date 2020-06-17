# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        name="hydra-pytest-plugin",
        version="1.0.0rc1",
        author="Omry Yadan",
        author_email="omry@fb.com",
        description="Hydra pytest plugin",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/facebookresearch/hydra/",
        packages=find_packages(include=["hydra_pytest_plugin"]),
        classifiers=["License :: OSI Approved :: MIT License", "Framework :: Pytest"],
        install_requires=["hydra-core~=1.0.0rc1"],
        # the following makes a plugin available to pytest
        entry_points={"pytest11": ["name_of_plugin = hydra_pytest_plugin"]},
    )
