# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging.config
import warnings
from typing import Any, Callable, Type, Union

from omegaconf import DictConfig, OmegaConf, _utils

from hydra.types import ObjectConf

log = logging.getLogger(__name__)


def _instantiate_class(
    clazz: Type[Any], config: Union[ObjectConf, DictConfig], *args: Any, **kwargs: Any
) -> Any:
    final_kwargs = _get_kwargs(config, **kwargs)
    return clazz(*args, **final_kwargs)


def _call_callable(
    fn: Callable[..., Any],
    config: Union[ObjectConf, DictConfig],
    *args: Any,
    **kwargs: Any,
) -> Any:
    final_kwargs = _get_kwargs(config, **kwargs)
    return fn(*args, **final_kwargs)


def _locate(path: str) -> Union[type, Callable[..., Any]]:
    """
    Locate an object by name or dotted path, importing as necessary.
    This is similar to the pydoc function `locate`, except that it checks for
    the module from the given path from back to front.
    """
    import builtins
    from importlib import import_module

    parts = [part for part in path.split(".") if part]
    module = None
    for n in reversed(range(len(parts))):
        try:
            module = import_module(".".join(parts[:n]))
        except Exception as e:
            if n == 0:
                log.error(f"Error loading module {path} : {e}")
                raise e
            continue
        if module:
            break
    if module:
        obj = module
    else:
        obj = builtins
    for part in parts[n:]:
        if not hasattr(obj, part):
            raise ValueError(
                f"Error finding attribute ({part}) in class ({obj.__name__}): {path}"
            )
        obj = getattr(obj, part)
    if isinstance(obj, type):
        obj_type: type = obj
        return obj_type
    elif callable(obj):
        obj_callable: Callable[..., Any] = obj
        return obj_callable
    else:
        # dummy case
        raise ValueError(f"Invalid type ({type(obj)}) found for {path}")


def _get_kwargs(config: Union[ObjectConf, DictConfig], **kwargs: Any) -> Any:
    import copy

    # copy config to avoid mutating it when merging with kwargs

    config_copy = copy.deepcopy(config)

    # Manually set parent as deepcopy does not currently handles it (https://github.com/omry/omegaconf/issues/130)
    # noinspection PyProtectedMember
    config_copy._set_parent(config._get_parent())  # type: ignore
    config = config_copy

    params = config.params if "params" in config else OmegaConf.create()
    assert isinstance(
        params, DictConfig
    ), f"Input config params are expected to be a mapping, found {type(config.params).__name__}"
    primitives = {}
    rest = {}
    for k, v in kwargs.items():
        if _utils.is_primitive_type(v) or isinstance(v, (dict, list)):
            primitives[k] = v
        else:
            rest[k] = v
    final_kwargs = {}
    params.merge_with(OmegaConf.create(primitives))
    for k, v in params.items():
        final_kwargs[k] = v

    for k, v in rest.items():
        final_kwargs[k] = v
    return final_kwargs


# private
def _get_cls_name(config: Union[ObjectConf, DictConfig]) -> str:
    if "class" in config:
        warnings.warn(
            "\n"
            "ObjectConf field 'class' is deprecated since Hydra 1.0.0 and will be removed in a future Hydra version.\n"
            "Offending config class:\n"
            f"\tclass={config['class']}\n"
            "Change your config to use 'cls' instead of 'class'.\n",
            category=UserWarning,
        )
        classname = config["class"]
        assert isinstance(classname, str)
        return classname
    else:
        if "cls" in config:
            return config.cls
        else:
            raise ValueError("Input config does not have a cls field")
