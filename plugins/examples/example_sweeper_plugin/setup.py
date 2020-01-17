# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        name="hydra-example-sweeper",
        version="0.1.0",
        author="Omry Yadan",
        author_email="omry@fb.com",
        description="Example Hydra Sweeper plugin",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/facebookresearch/hydra/",
        packages=find_packages(exclude=["tests", "example"]),
        classifiers=[
            # Feel free to choose another license
            "License :: OSI Approved :: MIT License",
            # Python versions are used by the noxfile in Hydra to determine which
            # python versions to test this plugin with
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Operating System :: OS Independent",
        ],
        install_requires=["hydra-core>=1.0.0rc1"],
        # If this plugin is providing configuration files, be sure to include them in the package.
        # See MANIFEST.in.
        # For configurations to be discoverable at runtime, they should also be added to the search path.
        include_package_data=True,
    )
