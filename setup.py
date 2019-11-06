# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import codecs
import distutils
import os
import re
import shutil
from os.path import join, exists, isdir

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


class CleanCommand(distutils.cmd.Command):
    """
    Our custom command to clean out junk files.
    """

    description = "Cleans out junk files we don't want in the repo"
    user_options = []

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
        description="Hydra is a library for writing flexible command line applications",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/facebookresearch/hydra",
        keywords="command-line configuration yaml tab-completion",
        packages=find_packages(),
        include_package_data=True,
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Development Status :: 4 - Beta",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Operating System :: POSIX :: Linux",
            "Operating System :: MacOS",
            "Operating System :: Microsoft :: Windows",
        ],
        install_requires=[
            "omegaconf>=1.4.0rc2",
            'pathlib2>=2.2.0;python_version<"3.0"',
        ],
        # Install development dependencies with
        # pip install -e .[dev]
        extras_require={
            "dev": [
                "black",
                "coverage",
                "flake8",
                "flake8-copyright",
                "nox",
                "pre-commit",
                "pytest",
                "setuptools",
                "towncrier",
                "twine",
            ]
        },
    )
