# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        name="hydra-ray-launcher",
        version="0.1.1",
        author="Badr Youbi Idrissi",
        author_email="badryoubiidrissi@gmail.com",
        description="Hydra basic ray launcher",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/BadrYoubiIdrissi/hydra-plugins",
        packages=find_packages(exclude=["tests", "example"]),
        classifiers=[
            # Feel free to choose another license
            "License :: OSI Approved :: MIT License",
            # Python versions are used by the noxfile in Hydra to determine which
            # python versions to test this plugin with
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Operating System :: OS Independent",
        ],
        install_requires=["hydra-core", "ray"],
        # If this plugin is providing configuration files, be sure to include them in the package.
        # See MANIFEST.in.
        # For configurations to be discoverable at runtime, they should also be added to the search path.
        include_package_data=True,
    )
