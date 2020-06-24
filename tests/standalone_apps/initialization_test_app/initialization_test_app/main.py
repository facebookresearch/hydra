# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import sys

from hydra.experimental import (
    compose,
    initialize,
    initialize_config_dir,
    initialize_config_module,
)


def main() -> None:
    with initialize(config_path="conf"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "main"

    with initialize(config_path="conf", job_name="test_job"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "test_job"

    abs_config_dir = os.path.abspath("initialization_test_app/conf")
    with initialize_config_dir(config_dir=abs_config_dir):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "app"

    with initialize_config_dir(config_dir=abs_config_dir, job_name="test_job"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "test_job"

    # Those tests can only work if the module is installed
    if len(sys.argv) > 1 and sys.argv[1] == "module_installed":
        with initialize_config_module(config_module="initialization_test_app.conf"):
            cfg = compose(config_name="config", return_hydra_config=True)
            assert cfg.config == {"hello": "world"}
            assert cfg.hydra.job.name == "app"

        with initialize_config_module(
            config_module="initialization_test_app.conf", job_name="test_job"
        ):
            cfg = compose(config_name="config", return_hydra_config=True)
            assert cfg.config == {"hello": "world"}
            assert cfg.hydra.job.name == "test_job"


if __name__ == "__main__":
    main()
