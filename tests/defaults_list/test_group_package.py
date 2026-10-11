# SPDX-FileCopyrightText: Contributors to Hydra
# SPDX-License-Identifier: MIT
from pathlib import Path
from typing import Any

from pytest import mark, param

from hydra import compose, initialize_config_dir
from hydra.core.default_element import ConfigDefault, GroupDefault, InputDefault
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
            "/preprocess@my_group_target: v1",
            "  - feature@relocated: default\n",
            [],
            {"relocated": {"my_group_target": {"version": "v1"}}},
            id="literal_group_package",
        ),
        param(
            "/preprocess/v1@my_group_target",
            "  - feature@relocated: default\n",
            [],
            {"relocated": {"my_group_target": {"version": "v1"}}},
            id="literal_config_package",
        ),
        param(
            "/preprocess@_group_.my_group_target: v1",
            "  - feature@relocated: default\n",
            [],
            {"preprocess": {"my_group_target": {"version": "v1"}}, "relocated": {}},
            id="literal_suffix",
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
            "override /preprocess@_group_: ${variant}",
            "  - variant: v1\n  - preprocess: v2\n  - feature@relocated: default\n",
            [],
            {"variant": {}, "preprocess": {"version": "v1"}, "relocated": {}},
            id="interpolated_override_value",
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
        param(
            None,
            "  - _self_\n",
            ["+preprocess@my_group_target=v1"],
            {"my_group_target": {"version": "v1"}},
            id="literal_cli_package",
        ),
        param(
            "/preprocess@_group_: v1",
            "  - feature@relocated: default\n",
            ["preprocess@_group_=v2"],
            {"preprocess": {"version": "v2"}, "relocated": {}},
            id="cli_symbolic_key",
        ),
        param(
            "/preprocess@_group_.suffix: v1",
            "  - feature@relocated: default\n",
            ["preprocess@_group_.suffix=v2"],
            {"preprocess": {"suffix": {"version": "v2"}}, "relocated": {}},
            id="cli_symbolic_suffix_key",
        ),
        param(
            "/preprocess@_group_: ${variant}",
            "  - variant: v1\n  - feature@relocated: default\n",
            ["preprocess=v2"],
            {"variant": {}, "preprocess": {"version": "v2"}, "relocated": {}},
            id="cli_overrides_interpolated_selection",
        ),
        param(
            "/preprocess@_group_: v1",
            "  - feature@relocated: default\n",
            ["~preprocess@_group_"],
            {"relocated": {}},
            id="cli_symbolic_delete",
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
    (tmp_path / "variant").mkdir()
    (tmp_path / "variant/v1.yaml").write_text("{}\n", encoding="utf-8")
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


@mark.parametrize(
    "default",
    [
        GroupDefault(group="user_group_settings", value="v1", package="_group_"),
        ConfigDefault(path="user_group_settings/v1", package="_group_"),
    ],
)
def test_group_package_parent_resolution_is_idempotent(default: InputDefault) -> None:
    default.update_parent("", "relocated")
    assert default.get_final_package() == "user_group_settings"
    default.update_parent("", "relocated")
    assert default.get_final_package() == "user_group_settings"


@mark.parametrize(
    "entry,overrides,expected_group",
    [
        param(
            "/group_a@_group_: ${prefix_group}/item",
            [],
            {"sub_group": {"x": 42}},
            id="group",
        ),
        param(
            "/group_a@_group_: ${prefix_group}/item",
            ["prefix_group=sub_other"],
            {"sub_other": {"x": 43}},
            id="cli_prefix_selection",
        ),
        param(
            "/group_a@_group_.suffix: ${prefix_group}/item",
            [],
            {"sub_group": {"suffix": {"x": 42}}},
            id="group_suffix",
        ),
        param(
            "/group_a/${prefix_group}/item@_group_",
            [],
            {"sub_group": {"x": 42}},
            id="config",
        ),
        param(
            "/group_a/${prefix_group}/item@_group_.suffix",
            [],
            {"sub_group": {"suffix": {"x": 42}}},
            id="config_suffix",
        ),
    ],
)
def test_group_package_interpolation(
    hydra_restore_singletons: Any,
    tmp_path: Path,
    entry: str,
    overrides: list[str],
    expected_group: Any,
) -> None:
    (tmp_path / "prefix_group").mkdir()
    (tmp_path / "feature").mkdir()
    (tmp_path / "group_a/sub_group").mkdir(parents=True)
    (tmp_path / "group_a/sub_other").mkdir()
    (tmp_path / "prefix_group/sub_group.yaml").write_text("{}\n", encoding="utf-8")
    (tmp_path / "prefix_group/sub_other.yaml").write_text("{}\n", encoding="utf-8")
    (tmp_path / "group_a/sub_group/item.yaml").write_text("x: 42\n", encoding="utf-8")
    (tmp_path / "group_a/sub_other/item.yaml").write_text("x: 43\n", encoding="utf-8")
    (tmp_path / "feature/default.yaml").write_text(
        f"defaults:\n  - {entry}\n", encoding="utf-8"
    )
    (tmp_path / "config.yaml").write_text(
        "defaults:\n  - prefix_group: sub_group\n  - feature@relocated: default\n",
        encoding="utf-8",
    )
    with initialize_config_dir(config_dir=str(tmp_path)):
        assert compose(config_name="config", overrides=overrides) == {
            "prefix_group": {},
            "group_a": expected_group,
            "relocated": {},
        }


def test_group_package_suffix_with_empty_group(tmp_path: Path) -> None:
    (tmp_path / "item.yaml").write_text("x: 42\n", encoding="utf-8")
    (tmp_path / "config.yaml").write_text(
        "defaults:\n  - /item@_group_.suffix\n", encoding="utf-8"
    )
    with initialize_config_dir(config_dir=str(tmp_path)):
        assert compose(config_name="config") == {"suffix": {"x": 42}}
