from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        name="hydra",
        version="0.1.0",
        author="Omry Yadan",
        author_email="omry@fb.com",
        description="Hydra is a generic experimentation framework for scientific computing and machine learning",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/fairinternal/hydra",
        keywords='experimentation',
        packages=['hydra'],
        include_package_data=True,
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            'omegaconf>=1.2.1',
            'setuptools',
            'fairtask@git+ssh://git@github.com/fairinternal/fairtask.git@master',
            'fairtask-slurm@git+ssh://git@github.com/fairinternal/fairtask-slurm.git@master',
            'submitit@git+ssh://git@github.com/fairinternal/submitit@master#egg=submitit'
        ],

        # Install development dependencies with
        # pip install -e .[dev]
        extras_require={
            'dev': [
                'coverage',
                'pytest',
                'tox',
                'twine',
                'six'
            ]
        }
    )
