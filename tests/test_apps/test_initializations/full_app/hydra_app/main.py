# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from hydra.experimental import (
    initialize_ctx,
    compose,
    initialize_config_dir_ctx,
    initialize_config_module_ctx,
)


def main() -> None:
    with initialize_ctx(config_path="conf"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "app"

    with initialize_config_dir_ctx(config_dir="conf"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "app"

    with initialize_config_module_ctx(config_module="hydra_app.conf"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "app"

    # overriding job name
    with initialize_ctx(config_path="conf", job_name="test_job"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "test_job"

    with initialize_config_dir_ctx(config_dir="conf", job_name="test_job"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "test_job"

    with initialize_config_module_ctx(
        config_module="hydra_app.conf", job_name="test_job"
    ):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "test_job"


if __name__ == "__main__":
    main()
