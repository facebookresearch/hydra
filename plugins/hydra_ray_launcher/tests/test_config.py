# SPDX-FileCopyrightText: Contributors to Hydra
# SPDX-License-Identifier: MIT
import sys
from importlib.metadata import version
from pathlib import Path

import pytest
from omegaconf import OmegaConf
from omegaconf.errors import InterpolationResolutionError

from hydra_plugins.hydra_ray_launcher import _config  # noqa: F401


@pytest.mark.parametrize(
    "name, distribution",
    [
        ("hydra", "hydra-core"),
        ("omegaconf", "omegaconf"),
        ("ray", "ray"),
        ("cloudpickle", "cloudpickle"),
        ("hydra_ray_launcher", "hydra-ray-launcher"),
    ],
)
def test_pkg_version(name: str, distribution: str) -> None:
    cfg = OmegaConf.create({"version": f"${{ray_pkg_version:{name}}}"})
    assert cfg.version == version(distribution)


@pytest.mark.parametrize("has_metadata", [False, True])
def test_pkg_version_does_not_import(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, has_metadata: bool
) -> None:
    name = "hydra_version_import_probe"
    (tmp_path / f"{name}.py").write_text("raise AssertionError('module imported')\n")
    if has_metadata:
        metadata = tmp_path / f"{name}-1.2.3.dist-info"
        metadata.mkdir()
        (metadata / "METADATA").write_text(
            f"Metadata-Version: 2.1\nName: {name}\nVersion: 1.2.3\n"
        )
    monkeypatch.syspath_prepend(str(tmp_path))
    cfg = OmegaConf.create({"version": f"${{ray_pkg_version:{name}}}"})
    if has_metadata:
        assert cfg.version == "1.2.3"
    else:
        with pytest.raises(InterpolationResolutionError, match="PackageNotFoundError"):
            _ = cfg.version
    assert name not in sys.modules
