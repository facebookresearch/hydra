# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import copy
import functools
import inspect
import os
from contextvars import ContextVar
from enum import Enum
from textwrap import dedent
from typing import Any, Callable, Dict, List, Sequence, Tuple, Union, cast

from omegaconf import AnyNode, OmegaConf, SCMode
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
        # detaching configs from parent.
        # At this time, everything is resolved and the parent link can cause
        # issues when serializing objects in some scenarios.
        for arg in args:
            if OmegaConf.is_config(arg):
                arg._set_parent(None)
        for v in kwargs.values():
            if OmegaConf.is_config(v):
                v._set_parent(None)
    except Exception as e:
        msg = (
            f"Error in collecting args and kwargs for '{_convert_target_to_string(_target_)}':"
            + f"\n{repr(e)}"
        )
        if full_key:
            msg += f"\nfull_key: {full_key}"

        raise InstantiationException(msg) from e

    if _partial_:
        try:
            return functools.partial(_target_, *args, **kwargs)
        except Exception as e:
            msg = (
                f"Error in creating partial({_convert_target_to_string(_target_)}, ...) object:"
                + f"\n{repr(e)}"
            )
            if full_key:
                msg += f"\nfull_key: {full_key}"
            raise InstantiationException(msg) from e
    else:
        try:
            return _target_(*args, **kwargs)
        except Exception as e:
            msg = f"Error in call to target '{_convert_target_to_string(_target_)}':\n{repr(e)}"
            if full_key:
                msg += f"\nfull_key: {full_key}"
            raise InstantiationException(msg) from e


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


def _prepare_input_dict_or_list(d: Union[Dict[Any, Any], List[Any]]) -> Any:
    res: Any
    if isinstance(d, dict):
        res = {}
        for k, v in d.items():
            if k == "_target_":
                v = _convert_target_to_string(d["_target_"])
            elif isinstance(v, (dict, list)):
                v = _prepare_input_dict_or_list(v)
            res[k] = v
    elif isinstance(d, list):
        res = []
        for v in d:
            if isinstance(v, (list, dict)):
                v = _prepare_input_dict_or_list(v)
            res.append(v)
    else:
        assert False
    return res


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
                    if full_key:
                        msg += f"\nfull_key: {full_key}"
                    raise InstantiationException(msg)
            _warn_legacy_target_whitelist(target_name)
        elif not _is_target_whitelisted(
            target_name, cast(Tuple[str, ...], target_whitelist)
        ):
            msg = dedent(f"""\
                Target '{target_name}' is not in the instantiate target whitelist.
                Pass _target_whitelist_ from trusted code to allow expected targets.""")
            if full_key:
                msg += f"\nfull_key: {full_key}"
            raise InstantiationException(msg)

        if isinstance(target, str):
            try:
                target = _locate(target)
            except Exception as e:
                msg = f"Error locating target '{target}', set env var HYDRA_FULL_ERROR=1 to see chained exception."
                if full_key:
                    msg += f"\nfull_key: {full_key}"
                raise InstantiationException(msg) from e
    if not callable(target):
        msg = f"Expected a callable target, got '{target}' of type '{type(target).__name__}'"
        if full_key:
            msg += f"\nfull_key: {full_key}"
        raise InstantiationException(msg)
    return target


def _deep_copy_full_config(subconfig: Any) -> Any:
    """Deep copy full config from root to leaf and return the copied subconfig"""
    if not OmegaConf.is_config(subconfig):
        return copy.deepcopy(subconfig)

    full_key = subconfig._get_full_key(None)
    if full_key == "" or full_key is None:  # Do not exit early if full_key is 0
        return copy.deepcopy(subconfig)
    full_key = str(full_key)

    if OmegaConf.is_list(subconfig._get_parent()):
        # OmegaConf has a bug where _get_full_key doesn't add [] if the parent
        # is a list, eg. instead of foo[0], it'll return foo0
        index = subconfig._key()
        full_key = full_key[: -len(str(index))] + f"[{index}]"
    root = subconfig._get_root()
    full_key = full_key.replace(root._get_full_key(None) or "", "", 1)
    if OmegaConf.select(root, full_key) is not subconfig:
        # The parent chain and full key are not consistent so don't
        # try to copy the full config
        return copy.deepcopy(subconfig)

    full_config_copy = copy.deepcopy(root)
    return OmegaConf.select(full_config_copy, full_key)


def instantiate(
    config: Any,
    *args: Any,
    _skip_instantiate_full_deepcopy_: bool = False,
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
                        none    : Passed objects are DictConfig and ListConfig, default
                        partial : Passed objects are converted to dict and list, with
                                  the exception of Structured Configs (and their fields).
                        object  : Passed objects are converted to dict and list.
                                  Structured Configs are converted to instances of the
                                  backing dataclass / attr class.
                        all     : Passed objects are dicts, lists and primitives without
                                  a trace of OmegaConf containers. Structured configs
                                  are converted to dicts / lists too.
                   _partial_: If True, return functools.partial wrapped method or object
                              False by default. Configure per target.
    :param _skip_instantiate_full_deepcopy_: If True, deep copy just the input config instead
                    of full config before resolving omegaconf interpolations, which may
                    potentially modify the config's parent/sibling configs in place.
                    False by default.
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

    if isinstance(config, (dict, list)):
        config = _prepare_input_dict_or_list(config)

    kwargs = _prepare_input_dict_or_list(kwargs)

    # Structured Config always converted first to OmegaConf
    if is_structured_config(config) or isinstance(config, (dict, list)):
        config = OmegaConf.structured(config, flags={"allow_objects": True})

    if OmegaConf.is_dict(config):
        # Finalize config (convert targets to strings, merge with kwargs)
        # Create copy to avoid mutating original
        if _skip_instantiate_full_deepcopy_:
            config_copy = copy.deepcopy(config)
            config_copy._set_parent(config._get_parent())
        else:
            config_copy = _deep_copy_full_config(config)
        config_copy._set_flag(
            flags=["allow_objects", "struct", "readonly"], values=[True, False, False]
        )
        config = config_copy

        if kwargs:
            config = OmegaConf.merge(config, kwargs)

        OmegaConf.resolve(config)

        _recursive_ = config.pop(_Keys.RECURSIVE, True)
        _convert_ = config.pop(_Keys.CONVERT, ConvertMode.NONE)
        _partial_ = config.pop(_Keys.PARTIAL, False)

        return instantiate_node(
            config,
            *args,
            recursive=_recursive_,
            convert=_convert_,
            partial=_partial_,
            target_whitelist=target_whitelist,
        )
    elif OmegaConf.is_list(config):
        # Finalize config (convert targets to strings, merge with kwargs)
        # Create copy to avoid mutating original
        if _skip_instantiate_full_deepcopy_:
            config_copy = copy.deepcopy(config)
            config_copy._set_parent(config._get_parent())
        else:
            config_copy = _deep_copy_full_config(config)
        config_copy._set_flag(
            flags=["allow_objects", "struct", "readonly"], values=[True, False, False]
        )
        config = config_copy

        OmegaConf.resolve(config)

        _recursive_ = kwargs.pop(_Keys.RECURSIVE, True)
        _convert_ = kwargs.pop(_Keys.CONVERT, ConvertMode.NONE)
        _partial_ = kwargs.pop(_Keys.PARTIAL, False)

        if _partial_:
            raise InstantiationException(
                "The _partial_ keyword is not compatible with top-level list instantiation"
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
                Top level config must be an OmegaConf DictConfig/ListConfig object,
                a plain dict/list, or a Structured Config class or instance.""")
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


def instantiate_node(
    node: Any,
    *args: Any,
    convert: Union[str, ConvertMode] = ConvertMode.NONE,
    recursive: bool = True,
    partial: bool = False,
    target_whitelist: NormalizedTargetWhitelist = None,
) -> Any:
    # Return None if config is None
    if node is None or (OmegaConf.is_config(node) and node._is_none()):
        return None

    if not OmegaConf.is_config(node):
        return node

    # Override parent modes from config if specified
    if OmegaConf.is_dict(node):
        # using getitem instead of get(key, default) because OmegaConf will raise an exception
        # if the key type is incompatible on get.
        convert = node[_Keys.CONVERT] if _Keys.CONVERT in node else convert
        recursive = node[_Keys.RECURSIVE] if _Keys.RECURSIVE in node else recursive
        partial = node[_Keys.PARTIAL] if _Keys.PARTIAL in node else partial

    full_key = node._get_full_key(None)

    if not isinstance(recursive, bool):
        msg = f"Instantiation: _recursive_ flag must be a bool, got {type(recursive)}"
        if full_key:
            msg += f"\nfull_key: {full_key}"
        raise TypeError(msg)

    if not isinstance(partial, bool):
        msg = f"Instantiation: _partial_ flag must be a bool, got {type(partial)}"
        if node and full_key:
            msg += f"\nfull_key: {full_key}"
        raise TypeError(msg)

    # If OmegaConf list, create new list of instances if recursive
    if OmegaConf.is_list(node):
        items = [
            instantiate_node(
                item,
                convert=convert,
                recursive=recursive,
                target_whitelist=target_whitelist,
            )
            for item in node._iter_ex(resolve=True)
        ]

        if convert in (ConvertMode.ALL, ConvertMode.PARTIAL, ConvertMode.OBJECT):
            # If ALL or PARTIAL or OBJECT, use plain list as container
            return items
        else:
            # Otherwise, use ListConfig as container
            lst = OmegaConf.create([], flags={"allow_objects": True})
            for item in items:
                lst.append(_wrap_structured_config_as_object(item))
            lst._set_parent(node)
            return lst

    elif OmegaConf.is_dict(node):
        if _Keys.TARGET_WHITELIST in node:
            msg = (
                "_target_whitelist_ must be passed to instantiate() from trusted "
                "code, not configured inside the config being instantiated."
            )
            if full_key:
                msg += f"\nfull_key: {full_key}"
            raise InstantiationException(msg)

        exclude_keys = set({"_target_", "_convert_", "_recursive_", "_partial_"})
        if _is_target(node):
            _target_ = _resolve_target(
                node.get(_Keys.TARGET), full_key, target_whitelist
            )
            kwargs = {}
            is_partial = node.get("_partial_", False) or partial
            for key in node.keys():
                if key not in exclude_keys:
                    if OmegaConf.is_missing(node, key) and is_partial:
                        continue
                    value = node[key]
                    if recursive:
                        value = instantiate_node(
                            value,
                            convert=convert,
                            recursive=recursive,
                            target_whitelist=target_whitelist,
                        )
                    kwargs[key] = _convert_node(value, convert)

            return _call_target(_target_, partial, args, kwargs, full_key)
        else:
            # If ALL or PARTIAL non structured or OBJECT non structured,
            # instantiate in dict and resolve interpolations eagerly.
            if convert == ConvertMode.ALL or (
                convert in (ConvertMode.PARTIAL, ConvertMode.OBJECT)
                and node._metadata.object_type in (None, dict)
            ):
                dict_items = {}
                for key, value in node.items():
                    # list items inherits recursive flag from the containing dict.
                    dict_items[key] = instantiate_node(
                        value,
                        convert=convert,
                        recursive=recursive,
                        target_whitelist=target_whitelist,
                    )
                return dict_items
            else:
                # Otherwise use DictConfig and resolve interpolations lazily.
                cfg = OmegaConf.create({}, flags={"allow_objects": True})
                for key, value in node.items():
                    cfg[key] = _wrap_structured_config_as_object(
                        instantiate_node(
                            value,
                            convert=convert,
                            recursive=recursive,
                            target_whitelist=target_whitelist,
                        )
                    )
                cfg._set_parent(node)
                cfg._metadata.object_type = node._metadata.object_type
                if convert == ConvertMode.OBJECT:
                    return OmegaConf.to_object(cfg)
                return cfg

    else:
        assert False, f"Unexpected config type : {type(node).__name__}"
