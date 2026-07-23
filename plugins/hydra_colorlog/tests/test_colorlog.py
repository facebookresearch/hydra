# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
from pathlib import Path

from hydra import initialize
from hydra.core.global_hydra import GlobalHydra
from hydra.test_utils.test_utils import chdir_plugin_root, run_python_script

chdir_plugin_root()


def test_config_installed() -> None:
    """
    Tests that color options are available for both hydra/hydra_logging and hydra/job_logging
    """

    with initialize(
        version_base=None, config_path="../hydra_plugins/hydra_colorlog/conf"
    ):
        config_loader = GlobalHydra.instance().config_loader()
        assert "colorlog" in config_loader.get_group_options("hydra/job_logging")
        assert "colorlog" in config_loader.get_group_options("hydra/hydra_logging")


def test_example_app_loads_its_config(tmp_path: Path) -> None:
    plugin_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(plugin_root)
        if pythonpath is None
        else os.pathsep.join([str(plugin_root), pythonpath])
    )
    stdout, _stderr = run_python_script(
        [
            str(plugin_root / "example" / "my_app.py"),
            f'hydra.run.dir="{tmp_path}"',
            "hydra.job.chdir=false",
        ],
        env=env,
    )

    assert "Info level message" in stdout
    assert (tmp_path / "my_app.log").exists()
