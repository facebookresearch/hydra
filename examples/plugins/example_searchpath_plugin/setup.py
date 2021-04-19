# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
from setuptools import find_namespace_packages, setup, find_packages


with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        name="hydra-example-searchpath-plugin",
        version="1.0.0",
        author="Omry Yadan",
        author_email="omry@fb.com",
        description="Example Hydra SearchPath plugin",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/facebookresearch/hydra/",
        packages=find_namespace_packages(include=["hydra_plugins.*"])
        + ["arbitrary_package"],
        classifiers=[
            # Feel free to use another license.
            "License :: OSI Approved :: MIT License",
            # Hydra uses Python version and Operating system to determine
            # In which environments to test this plugin
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            # consider pinning to a specific major version of Hydra to avoid unexpected
            # if a new major versio nof Hydra introduces introduces breaking changes for plugins.
            # e.g: "hydra-core==1.0.*",
            "hydra-core",
        ],
        # If this plugin is providing configuration files, be sure to include them in the package.
        # See MANIFEST.in.
        # For configurations to be discoverable at runtime, they should also be added to the search path.
        include_package_data=True,
    )
