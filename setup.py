import setuptools

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setuptools.setup(
        name="hydra",
        scripts=['bin/hydra'],
        version="0.1.0",
        author="Omry Yadan",
        author_email="omry@fb.com",
        description="Hydra is a generic experimentation framework for scientific computing and machine learning",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/fairinternal/hydra",
        keywords='experimentation',
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            'omegaconf>=1.1.3',
            'setuptools',
        ]
    )
