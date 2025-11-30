import setuptools

setuptools.setup(
    name="hydra-wandb-sweeper",
    version="0.0.1",
    author="Adrish Dey",
    author_email="adrish@wandb.com",
    description="Hydra sweeps with WandB sweeps",
    packages=setuptools.find_namespace_packages(include=["hydra_plugins.*"]),
    install_requires=["hydra-core", "wandb"],
    include_package_data=True,
)
