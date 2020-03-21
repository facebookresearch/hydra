# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging.config
import warnings
from pathlib import Path
from typing import Any, Type

from omegaconf import DictConfig, OmegaConf, _utils

from hydra.conf import PluginConf
from hydra.core.hydra_config import HydraConfig

log = logging.getLogger(__name__)


def get_method(path: str) -> type:
    return get_class(path)


def get_class(path: str) -> type:
    try:
        from pydoc import locate

        klass = locate(path)
        if not klass:
            log.error(f"Error finding module in class path {path}")
            raise ValueError(f"Error finding module in class path {path}")
        return klass
    except Exception as e:
        log.error(f"Error initializing class {path}")
        raise e


def get_static_method(full_method_name: str) -> type:
    try:
        ret: type = get_class(full_method_name)
        return ret
    except Exception as e:
        log.error("Error getting static method {} : {}".format(full_method_name, e))
        raise e


def instantiate(config: PluginConf, *args: Any, **kwargs: Any) -> Any:
    classname = _get_class_name(config)
    try:
        clazz = get_class(classname)
        return _instantiate_class(clazz, config, *args, **kwargs)
    except Exception as e:
        log.error(f"Error instantiating '{classname}' : {e}")
        raise e


def get_original_cwd() -> str:
    ret = HydraConfig.instance().hydra.runtime.cwd
    assert ret is not None and isinstance(ret, str)
    return ret


def to_absolute_path(path: str) -> str:
    """
    converts the specified path to be absolute path.
    if the input path is relative, it's interpreted as relative to the original working directory
    if it's absolute, it's returned as is
    :param path:
    :return:
    """
    p = Path(path)
    if p.is_absolute():
        ret = p
    else:
        ret = Path(get_original_cwd()) / p
    return str(ret)


def _get_class_name(config: PluginConf) -> str:
    if "class" in config:
        warnings.warn(
            "\n"
            "PluginConf field 'class' is deprecated since Hydra 1.0.0 and will be removed in a future Hydra version.\n"
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


def _instantiate_class(
    clazz: Type[Any], config: PluginConf, *args: Any, **kwargs: Any
) -> Any:
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
    ), "Input config params are expected to be a mapping, found {}".format(
        type(config.params)
    )
    primitives = {}
    rest = {}
    for k, v in kwargs.items():
        if _utils._is_primitive_type(v) or isinstance(v, (dict, list)):
            primitives[k] = v
        else:
            rest[k] = v
    final_kwargs = {}
    params.merge_with(OmegaConf.create(primitives))
    for k, v in params.items():
        final_kwargs[k] = v

    for k, v in rest.items():
        final_kwargs[k] = v

    return clazz(*args, **final_kwargs)
