# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
from pathlib import Path

from hydra.core.plugins import Plugins
from hydra.plugins.plugin import Plugin

# TODO: test that launcher and sweeper plugins are imported only once when they are instantiated


def test_number_of_imports(tmpdir: Path) -> None:
    os.environ["TMP_FILE"] = str(tmpdir / "import.log")
    # Tests that this plugin can be discovered via the plugins subsystem when looking at all Plugins
    assert "DiscoveryTestPlugin" in [x.__name__ for x in Plugins.discover(Plugin)]

    with Path(os.environ["TMP_FILE"]) as f:
        txt = str(f.read_text())
        assert txt.split("\n").count("imported") == 1
