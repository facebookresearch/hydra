# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
from pathlib import Path

from hydra.core.plugins import Plugins
from hydra.plugins.plugin import Plugin


def test_number_of_imports(tmpdir: Path) -> None:
    os.environ["TMP_FILE"] = str(tmpdir / "import.log")
    # Tests that this plugin can be discovered via the plugins subsystem when looking at all Plugins
    assert "DiscoveryTestPlugin" in [
        x.__name__ for x in Plugins.instance().discover(Plugin)
    ]

    with Path(os.environ["TMP_FILE"]) as f:
        txt = str(f.read_text())
        assert txt.split("\n").count("imported") == 1


def test_skipped_imports(tmpdir: Path) -> None:
    # Tests that modules starting with an "_" (but not "__") are skipped

    discovered_plugins = [x.__name__ for x in Plugins.instance().discover(Plugin)]
    assert "HiddenTestPlugin" not in discovered_plugins

    assert "NotHiddenTestPlugin" in discovered_plugins
