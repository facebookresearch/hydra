# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os

from hydra import compose, initialize, initialize_config_dir

if __name__ == "__main__":
    with initialize(version_base=None, config_path="."):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "main"

    with initialize(version_base=None, config_path=".", job_name="test_job"):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "test_job"

    abs_config__dir = os.path.abspath("")
    with initialize_config_dir(version_base=None, config_dir=abs_config__dir):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "app"

    with initialize_config_dir(
        version_base=None, config_dir=abs_config__dir, job_name="test_job"
    ):
        cfg = compose(config_name="config", return_hydra_config=True)
        assert cfg.config == {"hello": "world"}
        assert cfg.hydra.job.name == "test_job"
