# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import codecs
import os
import re

from setuptools import find_packages, setup


def find_version(*file_paths):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *file_paths), "r") as fp:
        version_file = fp.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        name="hydra-pytest-plugin",
        version=find_version("hydra_pytest_plugin", "__init__.py"),
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
