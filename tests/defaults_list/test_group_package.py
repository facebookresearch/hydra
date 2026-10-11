# SPDX-FileCopyrightText: Contributors to Hydra
# SPDX-License-Identifier: MIT
from pathlib import Path
from typing import Any

from pytest import mark, param

from hydra import compose, initialize_config_dir
from hydra.core.plugins import Plugins

Plugins.instance()


@mark.parametrize(
    "entry,root_defaults,overrides,expected",
    [
        param(
            "/preprocess@_group_: v1",
            "  - feature@relocated: default\n",
            [],
            {"preprocess": {"version": "v1"}, "relocated": {}},
            id="group_include",
        ),
        param(
            "/preprocess/v1@_group_",
            "  - feature@relocated: default\n",
            [],
            {"preprocess": {"version": "v1"}, "relocated": {}},
            id="config_include",
        ),
        param(
            "/preprocess@_group_.suffix: v1",
            "  - feature@relocated: default\n",
            [],
            {"preprocess": {"suffix": {"version": "v1"}}, "relocated": {}},
            id="group_suffix",
        ),
        param(
            "/preprocess/v1@_group_.suffix",
            "  - feature@relocated: default\n",
            [],
            {"preprocess": {"suffix": {"version": "v1"}}, "relocated": {}},
            id="config_suffix",
        ),
        param(
            "override /preprocess@_group_: v1",
            "  - preprocess: v2\n  - feature@relocated: default\n",
            [],
            {"preprocess": {"version": "v1"}, "relocated": {}},
            id="nested_override",
        ),
        param(
            "override /preprocess@_group_: v1",
            "  - preprocess: v2\n  - feature@relocated: default\n",
            ["preprocess=v2"],
            {"preprocess": {"version": "v2"}, "relocated": {}},
            id="cli_selection_wins",
        ),
        param(
            None,
            "  - _self_\n",
            ["+preprocess@_group_=v1"],
            {"preprocess": {"version": "v1"}},
            id="cli_package",
        ),
        param(
            None,
            "  - _self_\n",
            ["+preprocess@_group_.suffix=v1"],
            {"preprocess": {"suffix": {"version": "v1"}}},
            id="cli_package_suffix",
        ),
    ],
)
def test_group_package_composition(
    hydra_restore_singletons: Any,
    tmp_path: Path,
    recwarn: Any,
    entry: str | None,
    root_defaults: str,
    overrides: list[str],
    expected: Any,
) -> None:
    (tmp_path / "preprocess").mkdir()
    (tmp_path / "feature").mkdir()
    (tmp_path / "preprocess/v1.yaml").write_text("version: v1\n", encoding="utf-8")
    (tmp_path / "preprocess/v2.yaml").write_text("version: v2\n", encoding="utf-8")
    (tmp_path / "feature/default.yaml").write_text(
        "{}\n" if entry is None else f"defaults:\n  - {entry}\n",
        encoding="utf-8",
    )
    (tmp_path / "config.yaml").write_text(
        f"defaults:\n{root_defaults}", encoding="utf-8"
    )

    with initialize_config_dir(config_dir=str(tmp_path)):
        assert compose(config_name="config", overrides=overrides) == expected
    assert len(recwarn) == 0
