# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from hydra.experimental import (
    initialize_ctx,
    compose,
    initialize_config_dir_ctx,
    initialize_config_module_ctx,
)


if __name__ == "__main__":
    with initialize_ctx():
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "app"

    with initialize_config_dir_ctx(config_dir="."):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "app"

    # This works because pkg_resource is weird.
    # It may stop working if I switch to importlib_resources
    with initialize_config_module_ctx(config_module="main"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "app"

    # overriding job name
    with initialize_ctx(job_name="test_job"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "test_job"

    with initialize_config_dir_ctx(config_dir=".", job_name="test_job"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "test_job"

    with initialize_config_module_ctx(
        config_module="hydra_app.conf", job_name="test_job"
    ):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "test_job"
