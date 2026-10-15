# SPDX-FileCopyrightText: Contributors to Hydra
# SPDX-License-Identifier: MIT
from dataclasses import dataclass
from typing import Any

from omegaconf import MISSING, DictConfig, OmegaConf
from omegaconf.errors import ValidationError
from pytest import mark, raises

from hydra.utils import instantiate


@dataclass
class Config:
    _target_: str = "builtins.dict"
    count: int = 1
    alias: int = "${count}"  # type: ignore


@mark.parametrize("isolate", [None, False, True])
def test_missing_root_without_overrides(isolate: bool | None) -> None:
    config = DictConfig(MISSING, ref_type=Config)

    result = instantiate(
        config,
        _execution_whitelist_="builtins.dict",
        **({} if isolate is None else {"isolate": isolate}),
    )

    assert isinstance(result, DictConfig)
    assert result == {}
    assert config._is_missing()


def test_ordinary_root_isolation_default_precedes_overrides() -> None:
    config = OmegaConf.create(
        {
            "_target_": "builtins.dict",
            "_recursive_": False,
            "_isolate_": "${enabled}",
            "enabled": False,
            "payload": {"value": "${enabled}"},
        }
    )

    result = instantiate(config, enabled=True, _execution_whitelist_="builtins.dict")

    assert result["enabled"] is True
    assert OmegaConf.is_interpolation(result["payload"], "value")
    assert result["payload"]._get_parent() is not None


@mark.parametrize("value", [MISSING, None])
@mark.parametrize("isolate", [False, True])
@mark.parametrize("readonly", [False, True])
def test_structured_root_overrides(value: Any, isolate: bool, readonly: bool) -> None:
    config = DictConfig(value, ref_type=Config)
    OmegaConf.set_readonly(config, readonly)
    metadata = config._metadata

    result = instantiate(
        config, count=2, isolate=isolate, _execution_whitelist_="builtins.dict"
    )

    assert result == {"count": 2, "alias": 2}
    assert config._value() == value
    assert config._metadata is metadata
    assert OmegaConf.is_readonly(config) is readonly


@mark.parametrize("isolate", [False, True])
def test_untyped_missing_root_with_callsite_target(isolate: bool) -> None:
    config = DictConfig(MISSING)
    runtime_value = object()

    result = instantiate(
        config,
        _target_="builtins.dict",
        value=runtime_value,
        isolate=isolate,
        _execution_whitelist_="builtins.dict",
    )

    assert result["value"] is runtime_value
    assert config._is_missing()


@mark.parametrize("isolate", [False, True])
def test_missing_root_override_type_validation(isolate: bool) -> None:
    config = DictConfig(MISSING, ref_type=Config)

    with raises(ValidationError):
        instantiate(
            config, count="2", isolate=isolate, _execution_whitelist_="builtins.dict"
        )

    assert config._is_missing()


@mark.parametrize("isolate", [False, True])
def test_missing_node_preserves_ancestor_context(isolate: bool) -> None:
    @dataclass
    class ContextConfig:
        _target_: str = "builtins.dict"
        count: int = "${outside}"  # type: ignore

    root = OmegaConf.create(
        {"outside": 10, "node": DictConfig(MISSING, ref_type=ContextConfig)}
    )
    config = root._get_node("node")
    assert isinstance(config, DictConfig)

    result = instantiate(
        config, extra=2, isolate=isolate, _execution_whitelist_="builtins.dict"
    )

    assert result == {"count": 10, "extra": 2}
    assert OmegaConf.is_missing(root, "node")
    assert config._get_parent() is root
