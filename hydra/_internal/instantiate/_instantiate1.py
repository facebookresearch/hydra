# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any, Mapping, MutableMapping, Union

from omegaconf import DictConfig, OmegaConf
from omegaconf._utils import is_structured_config

from hydra._internal.utils import (
    _call_target,
    _convert_container_targets_to_strings,
    _is_target,
    _Keys,
    _resolve_target,
)
from hydra.errors import InstantiationException
from hydra.types import ConvertMode, TargetConf


def _merge_overrides_into_config(
    config: Union[MutableMapping[Any, Any], DictConfig], overrides: Mapping[Any, Any]
) -> None:
    """Merge overrides into config recursively."""

    def _rec_merge(a: Any, b: Any) -> Any:
        """Recursively merge mappings from b into a."""
        if isinstance(a, Mapping):
            if not isinstance(a, MutableMapping):
                raise TypeError(f"Expected type MutableMapping but got {type(a)}")
            for key, item in b.items():
                a[key] = _rec_merge(a[key], item) if key in a else item
            return a
        return b

    if OmegaConf.is_dict(config):
        assert isinstance(config, DictConfig)
        config.merge_with(OmegaConf.create(overrides, flags={"allow_objects": True}))  # type: ignore
    elif isinstance(config, MutableMapping):
        _rec_merge(config, overrides)
    else:
        raise TypeError(f"Expected DictConfig or MutableMapping but got {type(config)}")


def instantiate(
    config: Any,
    *args: Any,
    convert: Union[str, ConvertMode] = ConvertMode.NONE,
    recursive: bool = True,
    **kwargs: Any,
) -> Any:
    """
    :param config: An config object describing what to call and what params to use.
                   In addition to the parameters, the config must contain:
                   _target_ : target class or callable name (str)
                   And may contain:
                   _recursive_: Construct nested objects as well (bool).
                                True by default.
                                may be overridden via a _recursive_ key in
                                the kwargs
                   _convert_: Conversion strategy
                        none    : Passed objects are DictConfig and ListConfig, default
                        partial : Passed objects are converted to dict and list, with
                                  the exception of Structured Configs (and their fields).
                        all     : Passed objects are dicts, lists and primitives without
                                  a trace of OmegaConf containers
    :param args: Optional positional parameters pass-through
    :param kwargs: Optional named parameters to override
                   parameters in the config object. Parameters not present
                   in the config objects are being passed as is to the target.
    :param convert: Optional ConvertMode or str from parent. Will be
                    used if _convert_ is not set in kwargs or config.
    :param recursive: Optional bool from parent. Will be used if
                      _recursive is not set in kwargs or config.
    :return: if _target_ is a class name: the instantiated object
             if _target_ is a callable: the return value of the call
    """
    # Return None if config is None
    if config is None or OmegaConf.is_none(config):
        return None

    # TargetConf edge case
    if isinstance(config, TargetConf) and config._target_ == "???":
        # Specific check to give a good warning about failure to annotate _target_ as a string.
        raise InstantiationException(
            f"Missing value for {type(config).__name__}._target_. Check that it's properly annotated and overridden."
            f"\nA common problem is forgetting to annotate _target_ as a string : '_target_: str = ...'"
        )

    # Structured Config always converted first to OmegaConf
    if is_structured_config(config):
        config = OmegaConf.structured(config, flags={"allow_objects": True})

    # Make copy if config is a standard dictionary
    if isinstance(config, dict):

        def _rec_copy(d: Any) -> Any:
            """Copy dictionary and children."""
            if isinstance(d, dict):
                return {key: _rec_copy(value) for key, value in d.items()}
            return d

        config = _rec_copy(config)

    # If OmegaConf, copy, make it mutable and set parent for live interpolation
    if OmegaConf.is_config(config):
        config_copy = OmegaConf.structured(config, flags={"allow_objects": True})
        OmegaConf.set_readonly(config_copy, False)
        OmegaConf.set_struct(config_copy, False)
        config_copy._set_parent(config._get_parent())
        config = config_copy

    # Finalize config (convert targets to strings, merge with kwargs)
    # TODO: kwargs are used as a config now. If it contains dataclass
    # objects, they will be interpreted as config nodes in the
    # instantiation result. We might want to change that behavior.
    _convert_container_targets_to_strings(config)
    _convert_container_targets_to_strings(kwargs)
    if kwargs:
        _merge_overrides_into_config(config, kwargs)

    # Override parent modes from config if specified
    # Cannot use pop with default because of OmegaConf typed config
    # Also interpret python None as Mode.NONE
    if isinstance(config, dict) or OmegaConf.is_dict(config):
        convert = config.pop(_Keys.CONVERT) if _Keys.CONVERT in config else convert
        convert = ConvertMode(convert if convert is not None else ConvertMode.NONE)
        recursive = (
            config.pop(_Keys.RECURSIVE) if _Keys.RECURSIVE in config else recursive
        )
        if not isinstance(recursive, bool):
            raise TypeError(f"_recursive_ flag must be a bool, got {type(recursive)}")

    if isinstance(config, (dict, list)):
        config = OmegaConf.structured(config, flags={"allow_objects": True})

    # If list, create new list of instances if recursive else config
    if isinstance(config, list):
        if recursive:
            result = []
            for item in config:
                result.append(instantiate(item, convert=convert, recursive=recursive))
            return result
        else:
            return config

    # If OmegaConf list, create new list of instances if recursive
    if OmegaConf.is_list(config):
        if recursive:
            # If ALL or PARTIAL, instantiate in list
            if convert in (ConvertMode.ALL, ConvertMode.PARTIAL):
                return [
                    instantiate(item, convert=convert, recursive=recursive)
                    for item in config._iter_ex(resolve=True)
                ]

            # Otherwise, new OmegaConf container
            lst = OmegaConf.create([], flags={"allow_objects": True})
            lst._set_parent(config)
            for item in config._iter_ex(resolve=False):
                lst.append(instantiate(item, convert=convert, recursive=recursive))
            lst._metadata.object_type = config._metadata.object_type
            return lst

        else:
            if convert == ConvertMode.ALL:
                return OmegaConf.to_container(config, resolve=True)
            if convert == ConvertMode.PARTIAL:
                return OmegaConf.to_container(
                    config, resolve=True, exclude_structured_configs=True
                )
            return config

    if isinstance(config, dict):
        target = (
            _resolve_target(config.pop(_Keys.TARGET)) if _is_target(config) else None
        )
        if recursive:
            final_kwargs = {}
            for key, value in config.items():
                final_kwargs[key] = instantiate(
                    value, convert=convert, recursive=recursive
                )
        else:
            final_kwargs = config
        if target:
            return _call_target(target, *args, **final_kwargs)
        else:
            if args:
                raise ValueError(
                    f"No target found in config {config} but args = {args} (should be empty)"
                )
            return final_kwargs

    if OmegaConf.is_dict(config):
        if _is_target(config):
            target = _resolve_target(config.pop(_Keys.TARGET))
            if recursive:
                final_kwargs = {}
                for key, value in config.items_ex(resolve=True):
                    final_kwargs[key] = instantiate(
                        value, convert=convert, recursive=recursive
                    )
            else:
                final_kwargs = config
            return _call_target(target, *args, **final_kwargs)

        if recursive:
            # If ALL or PARTIAL non structured, instantiate in dict
            if convert == ConvertMode.ALL or (
                convert == ConvertMode.PARTIAL and config._metadata.object_type is None
            ):
                final_kwargs = {}
                for key, value in config.items_ex(resolve=True):
                    final_kwargs[key] = instantiate(
                        value, convert=convert, recursive=recursive
                    )
                return final_kwargs

            # Otherwise, new OmegaConf container
            cfg = OmegaConf.create({}, flags={"allow_objects": True})
            for key, value in config.items_ex(resolve=False):
                cfg[key] = instantiate(value, convert=convert, recursive=recursive)
            cfg._set_parent(config)
            cfg._metadata.object_type = config._metadata.object_type

            # If convert is PARTIAL, convert container
            if convert == ConvertMode.PARTIAL:
                return OmegaConf.to_container(
                    cfg, resolve=True, exclude_structured_configs=True
                )
            return cfg
        else:
            if convert == ConvertMode.ALL:
                return OmegaConf.to_container(config, resolve=True)
            if convert == ConvertMode.PARTIAL:
                return OmegaConf.to_container(
                    config, resolve=True, exclude_structured_configs=True
                )
            return config

    # Default case, return config (no target or recursive to handle)
    return config
