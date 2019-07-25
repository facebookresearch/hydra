import distutils
import os
from os.path import *

import shutil
from setuptools import setup, find_packages
import re


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
            '.eggs',
            '.egg-info',
            '.pytest_cache',
            'build',
            'dist',
            '__pycache__',
            '.pyc',
        ]
        deletion_list = CleanCommand.find('.', includes=delete_patterns, excludes=['\\.nox/.*'])

        for f in deletion_list:
            if exists(f):
                if isdir(f):
                    shutil.rmtree(f, ignore_errors=True)
                else:
                    os.unlink(f)


with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        cmdclass={
            'clean': CleanCommand,
        },
        name="hydra",
        version="0.1.0",
        author="Omry Yadan",
        author_email="omry@fb.com",
        description="Hydra is a generic experimentation framework for scientific computing and machine learning",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/fairinternal/hydra",
        keywords='experimentation',
        packages=find_packages(exclude=['tests']),
        include_package_data=True,
        classifiers=[
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.6",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            'omegaconf>=1.2.1',
        ],
        # Install development dependencies with
        # pip install -e .[dev]
        extras_require={
            'dev': [
                'pytest',
                'setuptools',
                'coverage',
            ]
        }
    )
