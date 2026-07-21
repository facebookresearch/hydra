# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import copy
import functools
import inspect
import os
from contextvars import ContextVar
from enum import Enum
from textwrap import dedent
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union, cast

from omegaconf import AnyNode, DictConfig, OmegaConf, SCMode
from omegaconf._utils import is_structured_config

from hydra._internal.deprecation_warning import deprecation_warning
from hydra._internal.utils import _locate
from hydra.errors import InstantiationException
from hydra.types import ConvertMode, TargetConf

DEFAULT_BLOCKLISTED_MODULES = {
    "builtins.exec",
    "builtins.eval",
    "builtins.__import__",
    "builtins.compile",
    "builtins.exit",
    "builtins.quit",
    "ctypes.CDLL",
    "ctypes.OleDLL",
    "ctypes.PyDLL",
    "ctypes.WinDLL",
    "ctypes.cdll.LoadLibrary",
    "ctypes.oledll.LoadLibrary",
    "ctypes.pydll.LoadLibrary",
    "ctypes.windll.LoadLibrary",
    "importlib.import_module",
    "os.kill",
    "os.system",
    "os.popen",
    "os.putenv",
    "os.remove",
    "os.removedirs",
    "os.rmdir",
    "os.fchdir",
    "os.setuid",
    "os.fork",
    "os.forkpty",
    "os.killpg",
    "os.rename",
    "os.renames",
    "os.startfile",
    "os.posix_spawn",
    "os.posix_spawnp",
    "os.truncate",
    "os.replace",
    "os.unlink",
    "os.fchmod",
    "os.fchown",
    "os.chmod",
    "os.chown",
    "os.chroot",
    "os.fchdir",
    "os.lchflags",
    "os.lchmod",
    "os.lchown",
    "os.getcwd",
    "os.chdir",
    "pty.spawn",
    "runpy.run_module",
    "runpy.run_path",
    "shutil.rmtree",
    "shutil.move",
    "shutil.chown",
    "subprocess.Popen",
    "subprocess.run",
    "subprocess.call",
    "subprocess.check_call",
    "subprocess.check_output",
    "subprocess.getoutput",
    "subprocess.getstatusoutput",
    "builtins.help",
    "sys.modules.ipdb",
    "sys.modules.joblib",
    "sys.modules.resource",
    "sys.modules.psutil",
    "sys.modules.tkinter",
}

DEFAULT_BLOCKLISTED_MODULE_PREFIXES = (
    "os.exec",
    "os.spawn",
)


class _UnsafeAllowAllTargets:
    def __repr__(self) -> str:
        return "UNSAFE_ALLOW_ALL_TARGETS"


UNSAFE_ALLOW_ALL_TARGETS = _UnsafeAllowAllTargets()
NormalizedTargetWhitelist = Union[Tuple[str, ...], _UnsafeAllowAllTargets, None]
ConfigOverlay = Union[Dict[str, Any], DictConfig]
_TARGET_WHITELIST_CONTEXT: ContextVar[NormalizedTargetWhitelist] = ContextVar(
    "hydra_instantiate_target_whitelist", default=None
)


def _get_os_alias_target(target: str) -> str:
    for module in ("posix", "nt"):
        module_prefix = f"{module}."
        if target.startswith(module_prefix):
            return f"os.{target[len(module_prefix) :]}"
    return target


class _Keys(str, Enum):
    """Special keys in configs used by instantiate."""

    TARGET = "_target_"
    CONVERT = "_convert_"
    RECURSIVE = "_recursive_"
    ARGS = "_args_"
    PARTIAL = "_partial_"
    TARGET_WHITELIST = "_target_whitelist_"


def _is_target(x: Any) -> bool:
    if isinstance(x, dict):
        return "_target_" in x
    if OmegaConf.is_dict(x):
        return "_target_" in x
    return False


def _is_blocklisted_target(target: str) -> bool:
    canonical_target = _get_os_alias_target(target)
    return (
        canonical_target in DEFAULT_BLOCKLISTED_MODULES
        or canonical_target.startswith(DEFAULT_BLOCKLISTED_MODULE_PREFIXES)
    )


def _validate_target_whitelist_pattern(pattern: Any) -> str:
    if not isinstance(pattern, str):
        raise InstantiationException(
            f"Invalid _target_whitelist_ entry '{pattern}': expected a string"
        )
    if pattern == "":
        raise InstantiationException("Invalid _target_whitelist_ entry: empty string")
    if "*" not in pattern:
        return pattern
    if pattern == "*" or not pattern.endswith(".*") or pattern.count("*") > 1:
        raise InstantiationException(
            dedent(f"""\
                Invalid _target_whitelist_ entry '{pattern}'. Only trailing '.*'
                package wildcards are supported. The wildcard '*' is not allowed
                as a target whitelist pattern. To preserve legacy all-target
                behavior, pass UNSAFE_ALLOW_ALL_TARGETS explicitly.""")
        )
    prefix = pattern[:-2]
    if prefix == "" or prefix.endswith("."):
        raise InstantiationException(
            f"Invalid _target_whitelist_ entry '{pattern}': missing package prefix"
        )
    return pattern


def _normalize_target_whitelist(
    target_whitelist: Any,
) -> NormalizedTargetWhitelist:
    if target_whitelist is None:
        return None
    if target_whitelist is UNSAFE_ALLOW_ALL_TARGETS:
        return UNSAFE_ALLOW_ALL_TARGETS
    if isinstance(target_whitelist, _TargetWhitelistPolicy):
        return target_whitelist.whitelist
    if isinstance(target_whitelist, str):
        return (_validate_target_whitelist_pattern(target_whitelist),)
    try:
        return tuple(
            _validate_target_whitelist_pattern(pattern) for pattern in target_whitelist
        )
    except TypeError as e:
        raise InstantiationException(
            "Invalid _target_whitelist_: expected a string, a sequence of strings, "
            "or UNSAFE_ALLOW_ALL_TARGETS"
        ) from e


def _combine_target_whitelists(
    base: NormalizedTargetWhitelist, extra: NormalizedTargetWhitelist
) -> NormalizedTargetWhitelist:
    if base is UNSAFE_ALLOW_ALL_TARGETS or extra is UNSAFE_ALLOW_ALL_TARGETS:
        return UNSAFE_ALLOW_ALL_TARGETS
    if base is None:
        return extra
    if extra is None:
        return base
    return tuple(
        dict.fromkeys(cast(Tuple[str, ...], base) + cast(Tuple[str, ...], extra))
    )


class _TargetWhitelistPolicy:
    def __init__(
        self, whitelist: NormalizedTargetWhitelist, reset: bool = False
    ) -> None:
        self.whitelist = whitelist
        self.reset = reset
        self._tokens: List[Any] = []

    def resolve(
        self, inherited: NormalizedTargetWhitelist
    ) -> NormalizedTargetWhitelist:
        if self.reset:
            return self.whitelist
        return _combine_target_whitelists(inherited, self.whitelist)

    def __enter__(self) -> "_TargetWhitelistPolicy":
        self._tokens.append(
            _TARGET_WHITELIST_CONTEXT.set(self.resolve(_TARGET_WHITELIST_CONTEXT.get()))
        )
        return self

    def __exit__(self, *args: Any) -> None:
        _TARGET_WHITELIST_CONTEXT.reset(self._tokens.pop())


TargetWhitelist = Union[
    str, Sequence[str], _UnsafeAllowAllTargets, _TargetWhitelistPolicy, None
]


def target_whitelist(target_whitelist: TargetWhitelist, reset: bool = False) -> Any:
    """
    Create a target whitelist object for hydra.utils.instantiate().

    The returned object can be used as a context manager to apply a whitelist to
    instantiate() calls in the current context, or passed to instantiate() as
    _target_whitelist_.

    :param target_whitelist: A target string, list of target strings, or
        UNSAFE_ALLOW_ALL_TARGETS. A trailing .* allows targets under a package
        prefix.
    :param reset: If True, ignore any outer target_whitelist() context.
        If False, add these targets to the current context.
    """
    return _TargetWhitelistPolicy(
        whitelist=_normalize_target_whitelist(target_whitelist),
        reset=reset,
    )


def _resolve_target_whitelist(
    target_whitelist: TargetWhitelist,
) -> NormalizedTargetWhitelist:
    inherited = _TARGET_WHITELIST_CONTEXT.get()
    if isinstance(target_whitelist, _TargetWhitelistPolicy):
        return target_whitelist.resolve(inherited)
    return _combine_target_whitelists(
        inherited, _normalize_target_whitelist(target_whitelist)
    )


def _is_target_whitelisted(target: str, target_whitelist: Tuple[str, ...]) -> bool:
    for pattern in target_whitelist:
        if pattern.endswith(".*"):
            prefix = pattern[:-2]
            if target.startswith(f"{prefix}."):
                return True
        elif target == pattern:
            return True
    return False


def _warn_legacy_target_whitelist(target: str) -> None:
    stacklevel = 1
    frame = inspect.currentframe()
    while frame is not None:
        if frame.f_code.co_filename != __file__:
            break
        stacklevel += 1
        frame = frame.f_back
    deprecation_warning(
        dedent(
            f"""\
            hydra.utils.instantiate() resolved _target_='{target}' with no
            _target_whitelist_. This preserves legacy behavior but is deprecated
            because config-controlled targets can execute arbitrary code. Pass a
            callsite target whitelist, or pass UNSAFE_ALLOW_ALL_TARGETS to
            explicitly keep legacy behavior.
            See https://hydra.cc/docs/upgrades/1.3_to_1.4/instantiate_target_whitelist/"""
        ),
        stacklevel=stacklevel,
    )


def _extract_pos_args(input_args: Any, kwargs: Any) -> Tuple[Any, Any]:
    config_args = kwargs.pop(_Keys.ARGS, ())
    output_args = config_args

    if isinstance(config_args, Sequence):
        if len(input_args) > 0:
            output_args = input_args
    else:
        raise InstantiationException(
            f"Unsupported _args_ type: '{type(config_args).__name__}'. value: '{config_args}'"
        )

    return output_args, kwargs


def _with_full_key(message: str, full_key: str) -> str:
    return f"{message}\nfull_key: {full_key}" if full_key else message


def _call_target(
    _target_: Callable[..., Any],
    _partial_: bool,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
    full_key: str,
) -> Any:
    """Call target (type) with args and kwargs."""
    try:
        args, kwargs = _extract_pos_args(args, kwargs)
        args = tuple(_prepare_call_argument(arg) for arg in args)
        kwargs = {key: _prepare_call_argument(value) for key, value in kwargs.items()}
    except Exception as e:
        msg = (
            f"Error in collecting args and kwargs for '{_convert_target_to_string(_target_)}':"
            + f"\n{repr(e)}"
        )
        raise InstantiationException(_with_full_key(msg, full_key)) from e

    try:
        if _partial_:
            return functools.partial(_target_, *args, **kwargs)
        return _target_(*args, **kwargs)
    except Exception as e:
        if _partial_:
            msg = (
                f"Error in creating partial({_convert_target_to_string(_target_)}, ...) object:"
                + f"\n{repr(e)}"
            )
        else:
            msg = f"Error in call to target '{_convert_target_to_string(_target_)}':\n{repr(e)}"
        raise InstantiationException(_with_full_key(msg, full_key)) from e


def _convert_target_to_string(t: Any) -> Any:
    if callable(t) and hasattr(t, "__qualname__"):
        return f"{t.__module__}.{t.__qualname__}"
    else:
        return t


def _get_target_name_for_check(target: Union[str, type, Callable[..., Any]]) -> str:
    if isinstance(target, str):
        return target
    if hasattr(target, "__qualname__"):
        return f"{target.__module__}.{target.__qualname__}"
    target_type = type(target)
    return f"{target_type.__module__}.{target_type.__qualname__}"


def _prepare_input_container(
    d: Union[Dict[Any, Any], List[Any], Tuple[Any, ...]],
) -> Any:
    if isinstance(d, dict):
        result = {}
        for k, v in d.items():
            if k == "_target_":
                v = _convert_target_to_string(d["_target_"])
            else:
                v = _prepare_input_value(v)
            result[k] = v
        return result

    if isinstance(d, list) or type(d) is tuple:
        values = [_prepare_input_value(v) for v in d]
        return values if isinstance(d, list) else tuple(values)

    assert False


def _prepare_input_value(
    value: Any,
) -> Any:
    if isinstance(value, (dict, list)) or type(value) is tuple:
        return _prepare_input_container(value)
    return value


def _resolve_target(
    target: Union[str, type, Callable[..., Any]],
    full_key: str,
    target_whitelist: NormalizedTargetWhitelist = None,
) -> Union[type, Callable[..., Any]]:
    """Resolve target string, type or callable into type or callable."""
    if isinstance(target, str) or callable(target):
        target_name = _get_target_name_for_check(target)
        if target_whitelist is UNSAFE_ALLOW_ALL_TARGETS:
            pass
        elif target_whitelist is None:
            if _is_blocklisted_target(target_name):
                allowlist = os.environ.get("HYDRA_INSTANTIATE_ALLOWLIST_OVERRIDE", "")
                allowlist_entries = allowlist.split(":")
                canonical_target = _get_os_alias_target(target_name)
                if (
                    target_name not in allowlist_entries
                    and canonical_target not in allowlist_entries
                ):
                    msg = dedent(
                        f"""\
                        Target '{target_name}' is blocklisted and cannot be instantiated from config
                        to prevent security vulnerabilities, set env var
                        HYDRA_INSTANTIATE_ALLOWLIST_OVERRIDE={target_name}:<other allowlisted targets> to bypass"""
                    )
                    raise InstantiationException(_with_full_key(msg, full_key))
            _warn_legacy_target_whitelist(target_name)
        elif not _is_target_whitelisted(
            target_name, cast(Tuple[str, ...], target_whitelist)
        ):
            msg = dedent(f"""\
                Target '{target_name}' is not in the instantiate target whitelist.
                Pass _target_whitelist_ from trusted code to allow expected targets.""")
            raise InstantiationException(_with_full_key(msg, full_key))

        if isinstance(target, str):
            try:
                target = _locate(target)
            except Exception as e:
                msg = f"Error locating target '{target}', set env var HYDRA_FULL_ERROR=1 to see chained exception."
                raise InstantiationException(_with_full_key(msg, full_key)) from e
    if not callable(target):
        msg = f"Expected a callable target, got '{target}' of type '{type(target).__name__}'"
        raise InstantiationException(_with_full_key(msg, full_key))
    return target


def _prepare_call_argument(value: Any) -> Any:
    if OmegaConf.is_config(value):
        parent = value._get_parent()
        value = copy.deepcopy(value)
        value._set_parent(parent)
        value._set_flag("readonly", False)
        OmegaConf.resolve(value)
        value._set_parent(None)
    return value


def instantiate(
    config: Any,
    *args: Any,
    _target_whitelist_: TargetWhitelist = None,
    **kwargs: Any,
) -> Any:
    """
    :param config: An config object describing what to call and what params to use.
                   In addition to the parameters, the config must contain:
                   _target_ : target class or callable name (str)
                              IMPORTANT: This may pose a security risk since the config
                              can be used to execute arbitrary code. Make sure to use this only
                              with trusted configs or configure the target whitelist.
                   And may contain:
                   _args_: List-like of positional arguments to pass to the target
                   _recursive_: Construct nested objects as well (bool).
                                True by default.
                                may be overridden via a _recursive_ key in
                                the kwargs
                   _convert_: Conversion strategy
                        none    : Passed objects are DictConfig, ListConfig and
                                  TupleConfig, default
                        partial : Passed objects are converted to dict, list and
                                  tuple, with the exception of Structured Configs
                                  (and their fields).
                        object  : Passed objects are converted to dict, list and tuple.
                                  Structured Configs are converted to instances of the
                                  backing dataclass / attr class.
                        all     : Passed objects are dicts, lists, tuples and
                                  primitives without a trace of OmegaConf containers.
                                  Structured configs are converted to primitive
                                  containers too.
                   _partial_: If True, return functools.partial wrapped method or object
                              False by default. Configure per target.
    :param _target_whitelist_: A target string, list of target strings,
                    target_whitelist() policy, or UNSAFE_ALLOW_ALL_TARGETS. A trailing
                    .* allows targets under a package prefix. Passing None preserves
                    legacy behavior unless a target_whitelist() context is active.
    :param args: Optional positional parameters pass-through
    :param kwargs: Optional named parameters to override
                   parameters in the config object. Parameters not present
                   in the config objects are being passed as is to the target.
                   IMPORTANT: dataclasses instances in kwargs are interpreted as config
                              and cannot be used as passthrough
    :return: if _target_ is a class name: the instantiated object
             if _target_ is a callable: the return value of the call
    """

    # Return None if config is None
    if config is None:
        return None

    target_whitelist = _resolve_target_whitelist(_target_whitelist_)

    # TargetConf edge case
    if isinstance(config, TargetConf) and config._target_ == "???":
        # Specific check to give a good warning about failure to annotate _target_ as a string.
        raise InstantiationException(
            dedent(
                f"""\
                Config has missing value for key `_target_`, cannot instantiate.
                Config type: {type(config).__name__}
                Check that the `_target_` key in your dataclass is properly annotated and overridden.
                A common problem is forgetting to annotate _target_ as a string : '_target_: str = ...'"""
            )
        )
        # TODO: print full key

    if isinstance(config, (dict, list)) or type(config) is tuple:
        config = _prepare_input_container(config)

    kwargs = _prepare_input_container(kwargs)

    # Structured Config always converted first to OmegaConf
    if (
        is_structured_config(config)
        or isinstance(config, (dict, list))
        or type(config) is tuple
    ):
        config = OmegaConf.structured(config, flags={"allow_objects": True})

    if OmegaConf.is_dict(config):
        return instantiate_node(
            config,
            *args,
            overrides=kwargs,
            is_root=True,
            target_whitelist=target_whitelist,
        )
    elif OmegaConf.is_sequence(config):
        _recursive_ = kwargs.pop(_Keys.RECURSIVE, True)
        _convert_ = kwargs.pop(_Keys.CONVERT, ConvertMode.NONE)
        _partial_ = kwargs.pop(_Keys.PARTIAL, False)

        if _partial_:
            sequence_type = "tuple" if OmegaConf.is_tuple(config) else "list"
            raise InstantiationException(
                "The _partial_ keyword is not compatible with "
                f"top-level {sequence_type} instantiation"
            )

        return instantiate_node(
            config,
            *args,
            recursive=_recursive_,
            convert=_convert_,
            partial=_partial_,
            target_whitelist=target_whitelist,
        )
    else:
        raise InstantiationException(
            dedent(f"""\
                Cannot instantiate config of type {type(config).__name__}.
                Top level config must be an OmegaConf DictConfig/ListConfig/TupleConfig object,
                a plain dict/list/tuple, or a Structured Config class or instance.""")
        )


def _convert_node(node: Any, convert: Union[ConvertMode, str]) -> Any:
    if OmegaConf.is_config(node):
        if convert == ConvertMode.ALL:
            node = OmegaConf.to_container(node, resolve=True)
        elif convert == ConvertMode.PARTIAL:
            node = OmegaConf.to_container(
                node, resolve=True, structured_config_mode=SCMode.DICT_CONFIG
            )
        elif convert == ConvertMode.OBJECT:
            node = OmegaConf.to_container(
                node, resolve=True, structured_config_mode=SCMode.INSTANTIATE
            )
    return node


def _wrap_structured_config_as_object(value: Any) -> Any:
    if is_structured_config(value):
        return AnyNode(value, flags={"allow_objects": True})
    return value


def _create_sequence_result(
    items: List[Any],
    *,
    is_tuple: bool,
    convert: Union[str, ConvertMode],
    parent: Any = None,
) -> Any:
    if convert in (ConvertMode.ALL, ConvertMode.PARTIAL, ConvertMode.OBJECT):
        return tuple(items) if is_tuple else items

    if is_tuple:
        result = OmegaConf.create(
            tuple(_wrap_structured_config_as_object(item) for item in items),
            flags={"allow_objects": True},
        )
    else:
        result = OmegaConf.create([], flags={"allow_objects": True})
        for item in items:
            result.append(_wrap_structured_config_as_object(item))
    if parent is not None:
        result._set_parent(parent)
    return result


def _get_dict_override(value: Any) -> Optional[ConfigOverlay]:
    if isinstance(value, dict):
        return value
    if OmegaConf.is_dict(value):
        return cast(DictConfig, value)
    if is_structured_config(value) and not isinstance(value, type):
        config = OmegaConf.structured(value, flags={"allow_objects": True})
        assert OmegaConf.is_dict(config)
        return cast(DictConfig, config)
    return None


def _iter_effective_keys(node: Any, overrides: Optional[ConfigOverlay]) -> List[str]:
    keys = list(node.keys())
    if overrides:
        keys.extend(key for key in overrides if key not in keys)
    return keys


def _get_effective_control(
    node: Any,
    overrides: Optional[ConfigOverlay],
    key: _Keys,
    default: Any,
) -> Any:
    if overrides is not None and key in overrides:
        return overrides[key]
    return node[key] if key in node else default


def _is_missing_parameter(
    node: Any, overrides: Optional[ConfigOverlay], key: str
) -> bool:
    if overrides is not None and key in overrides:
        return isinstance(overrides[key], str) and overrides[key] == "???"
    return OmegaConf.is_missing(node, key)


def _instantiate_override(
    value: Any,
    *,
    convert: Union[str, ConvertMode],
    recursive: bool,
    target_whitelist: NormalizedTargetWhitelist,
) -> Any:
    dict_override = _get_dict_override(value)
    if not recursive:
        if isinstance(dict_override, DictConfig) and (
            dict_override._metadata.object_type not in (None, dict)
        ):
            return dict_override
        return value

    if dict_override is not None:
        return instantiate_node(
            OmegaConf.create({}),
            overrides=dict_override,
            convert=convert,
            recursive=recursive,
            target_whitelist=target_whitelist,
        )

    if isinstance(value, (list, tuple)):
        items = [
            _instantiate_override(
                item,
                convert=convert,
                recursive=recursive,
                target_whitelist=target_whitelist,
            )
            for item in value
        ]
        return _create_sequence_result(
            items, is_tuple=isinstance(value, tuple), convert=convert
        )

    if OmegaConf.is_config(value):
        return instantiate_node(
            value,
            convert=convert,
            recursive=recursive,
            target_whitelist=target_whitelist,
        )
    return value


def _instantiate_effective_value(
    node: Any,
    key: str,
    overrides: Optional[ConfigOverlay],
    *,
    convert: Union[str, ConvertMode],
    recursive: bool,
    target_whitelist: NormalizedTargetWhitelist,
) -> Any:
    if overrides is not None and key in overrides:
        override = overrides[key]
        dict_override = _get_dict_override(override)
        if recursive and dict_override is not None:
            configured_value = node._get_node(key) if key in node else None
            if not OmegaConf.is_dict(configured_value):
                configured_value = OmegaConf.create({})
            return instantiate_node(
                configured_value,
                overrides=dict_override,
                convert=convert,
                recursive=recursive,
                target_whitelist=target_whitelist,
            )
        return _instantiate_override(
            override,
            convert=convert,
            recursive=recursive,
            target_whitelist=target_whitelist,
        )

    value = node[key]
    if recursive:
        value = instantiate_node(
            value,
            convert=convert,
            recursive=recursive,
            target_whitelist=target_whitelist,
        )
    return value


def instantiate_node(
    node: Any,
    *args: Any,
    overrides: Optional[ConfigOverlay] = None,
    convert: Union[str, ConvertMode] = ConvertMode.NONE,
    recursive: bool = True,
    partial: bool = False,
    is_root: bool = False,
    target_whitelist: NormalizedTargetWhitelist = None,
) -> Any:
    # Return None if config is None
    if node is None or (
        OmegaConf.is_config(node) and node._is_none() and not overrides
    ):
        return None

    if OmegaConf.is_config(node) and node._is_none() and overrides:
        ref_type = node._metadata.ref_type
        parent = node._get_parent()
        key = node._key()
        node = (
            OmegaConf.structured(ref_type)
            if is_structured_config(ref_type)
            else OmegaConf.create({})
        )
        node._set_parent(parent)
        node._set_key(key)

    if not OmegaConf.is_config(node):
        return node

    # Override parent modes from config if specified
    if OmegaConf.is_dict(node):
        # using getitem instead of get(key, default) because OmegaConf will raise an exception
        # if the key type is incompatible on get.
        convert = _get_effective_control(node, overrides, _Keys.CONVERT, convert)
        recursive = _get_effective_control(node, overrides, _Keys.RECURSIVE, recursive)
        partial = _get_effective_control(node, overrides, _Keys.PARTIAL, partial)

    full_key = node._get_full_key(None)

    if not isinstance(recursive, bool):
        msg = f"Instantiation: _recursive_ flag must be a bool, got {type(recursive)}"
        raise TypeError(_with_full_key(msg, full_key))

    if not isinstance(partial, bool):
        msg = f"Instantiation: _partial_ flag must be a bool, got {type(partial)}"
        if node and full_key:
            msg += f"\nfull_key: {full_key}"
        raise TypeError(msg)

    # If OmegaConf sequence, create a new sequence of instances if recursive
    if OmegaConf.is_sequence(node):
        is_tuple = OmegaConf.is_tuple(node)
        items = [
            instantiate_node(
                item,
                convert=convert,
                recursive=recursive,
                target_whitelist=target_whitelist,
            )
            for item in node._iter_ex(resolve=True)
        ]

        return _create_sequence_result(
            items, is_tuple=is_tuple, convert=convert, parent=node
        )

    elif OmegaConf.is_dict(node):
        if _Keys.TARGET_WHITELIST in node:
            msg = (
                "_target_whitelist_ must be passed to instantiate() from trusted "
                "code, not configured inside the config being instantiated."
            )
            raise InstantiationException(_with_full_key(msg, full_key))

        exclude_keys = set({"_target_", "_convert_", "_recursive_", "_partial_"})
        if (overrides is not None and _Keys.TARGET in overrides) or _is_target(node):
            target = (
                overrides[_Keys.TARGET]
                if overrides is not None and _Keys.TARGET in overrides
                else node.get(_Keys.TARGET)
            )
            _target_ = _resolve_target(target, full_key, target_whitelist)
            kwargs = {}
            is_partial = partial
            for key in _iter_effective_keys(node, overrides):
                if key not in exclude_keys:
                    if is_partial and _is_missing_parameter(node, overrides, key):
                        continue
                    value = _instantiate_effective_value(
                        node,
                        key,
                        overrides,
                        convert=convert,
                        recursive=recursive,
                        target_whitelist=target_whitelist,
                    )
                    kwargs[key] = _convert_node(value, convert)

            return _call_target(_target_, partial, args, kwargs, full_key)
        else:
            object_type = node._metadata.object_type
            if isinstance(overrides, DictConfig):
                override_type = overrides._metadata.object_type
                if override_type not in (None, dict):
                    object_type = override_type

            # If ALL or PARTIAL non structured or OBJECT non structured,
            # instantiate in dict and resolve interpolations eagerly.
            if convert == ConvertMode.ALL or (
                convert in (ConvertMode.PARTIAL, ConvertMode.OBJECT)
                and object_type in (None, dict)
            ):
                dict_items = {}
                for key in _iter_effective_keys(node, overrides):
                    if is_root and key in exclude_keys:
                        continue
                    # list items inherits recursive flag from the containing dict.
                    dict_items[key] = _instantiate_effective_value(
                        node,
                        key,
                        overrides,
                        convert=convert,
                        recursive=recursive,
                        target_whitelist=target_whitelist,
                    )
                return dict_items
            else:
                # Otherwise use DictConfig and resolve interpolations lazily.
                cfg = OmegaConf.create({}, flags={"allow_objects": True})
                for key in _iter_effective_keys(node, overrides):
                    if is_root and key in exclude_keys:
                        continue
                    cfg[key] = _wrap_structured_config_as_object(
                        _instantiate_effective_value(
                            node,
                            key,
                            overrides,
                            convert=convert,
                            recursive=recursive,
                            target_whitelist=target_whitelist,
                        )
                    )
                cfg._set_parent(node)
                cfg._metadata.object_type = object_type
                if convert == ConvertMode.OBJECT:
                    return OmegaConf.to_object(cfg)
                return cfg

    else:
        assert False, f"Unexpected config type : {type(node).__name__}"
