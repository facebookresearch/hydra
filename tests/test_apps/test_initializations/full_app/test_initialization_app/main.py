# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import sys

from hydra.experimental import (
    compose,
    initialize_config_dir_ctx,
    initialize_config_module_ctx,
    initialize_ctx,
)


def main() -> None:
    with initialize_ctx(config_path="conf"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "app"

    with initialize_ctx(config_path="conf", job_name="test_job"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "test_job"

    with initialize_config_dir_ctx(config_dir="conf"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "app"

    with initialize_config_dir_ctx(config_dir="conf", job_name="test_job"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "test_job"

    # Those tests can only work if the module is installed
    if len(sys.argv) > 1 and sys.argv[1] == "module_installed":
        with initialize_config_module_ctx(config_module="test_initialization_app.conf"):
            cfg = compose(config_name="config", return_hydra_config=True)
            assert cfg.config == {"hello": "world"}
            assert cfg.hydra.job.name == "app"

        with initialize_config_module_ctx(
            config_module="test_initialization_app.conf", job_name="test_job"
        ):
            cfg = compose(config_name="config", return_hydra_config=True)
            assert cfg.config == {"hello": "world"}
            assert cfg.hydra.job.name == "test_job"


if __name__ == "__main__":
    main()
