# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
from setuptools import find_namespace_packages, setup

with open("README.md") as fh:
    LONG_DESC = fh.read()
    setup(
        name="hydra-example-generic-plugin",
        version="1.0.0",
        author="Omry Yadan",
        author_email="omry@fb.com",
        description="Example Hydra plugin",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/facebookresearch/hydra/",
        packages=find_namespace_packages(include=["hydra_plugins.*"]),
        classifiers=[
            # Feel free to use another license.
            "License :: OSI Approved :: MIT License",
            # Hydra uses Python version and Operating system to determine
            # In which environments to test this plugin
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            # consider pinning to a specific major version of Hydra to avoid unexpected problems
            # if a new major version of Hydra introduces breaking changes for plugins.
            # e.g: "hydra-core==1.0.*",
            "hydra-core",
        ],
        # See MANIFEST.in.
        # For configurations to be discoverable at runtime, they should also be added to the search path.
        include_package_data=True,
    )
