# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
import codecs
import os
import pathlib
import re
import shutil
from distutils import cmd
from os.path import exists, isdir, join
from typing import Any, List

import pkg_resources
from setuptools import find_packages, setup


def find_version(*file_paths):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *file_paths), "r") as fp:
        version_file = fp.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with pathlib.Path("requirements/requirements.txt").open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement in pkg_resources.parse_requirements(requirements_txt)
    ]


class CleanCommand(cmd.Command):
    """
    Our custom command to clean out junk files.
    """

    description = "Cleans out junk files we don't want in the repo"
    user_options: List[Any] = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def find(root, includes, excludes=[]):
        res = []
        for parent, dirs, files in os.walk(root):
            for f in dirs + files:
                add = list()
                for include in includes:
                    if re.findall(include, f):
                        add.append(join(parent, f))
                res.extend(add)
        final_list = []
        # Exclude things that matches an exclude pattern
        for ex in excludes:
            for file in res:
                if not re.findall(ex, file):
                    final_list.append(file)
        return final_list

    def run(self):
        delete_patterns = [
            ".eggs",
            ".egg-info",
            ".pytest_cache",
            "build",
            "dist",
            "__pycache__",
            ".pyc",
        ]
        deletion_list = CleanCommand.find(
            ".", includes=delete_patterns, excludes=["\\.nox/.*"]
        )

        for f in deletion_list:
            if exists(f):
                if isdir(f):
                    shutil.rmtree(f, ignore_errors=True)
                else:
                    os.unlink(f)


with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        cmdclass={"clean": CleanCommand},
        name="hydra-core",
        version=find_version("hydra", "__init__.py"),
        author="Omry Yadan",
        author_email="omry@fb.com",
        description="A framework for elegantly configuring complex applications",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/facebookresearch/hydra",
        keywords="command-line configuration yaml tab-completion",
        packages=find_packages(include=["hydra"]),
        include_package_data=True,
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Development Status :: 4 - Beta",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Operating System :: POSIX :: Linux",
            "Operating System :: MacOS",
            "Operating System :: Microsoft :: Windows",
        ],
        install_requires=install_requires,
        entry_points={"pytest11": ["hydra_pytest = hydra.extra.pytest_plugin"]},
        # Install development dependencies with
        # pip install -r requirements/dev.txt -e .
    )
