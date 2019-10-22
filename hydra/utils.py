# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging.config

from omegaconf import OmegaConf

from hydra._internal.pathlib import Path
from hydra.plugins.common.utils import HydraConfig

# pylint: disable=C0103
log = logging.getLogger(__name__)


def get_method(path):
    return get_class(path)


def get_class(path):
    try:
        from importlib import import_module

        module_path, _, class_name = path.rpartition(".")
        mod = import_module(module_path)
        try:
            klass = getattr(mod, class_name)
        except AttributeError:
            raise ImportError(
                "Class {} is not in module {}".format(class_name, module_path)
            )
        return klass
    except ValueError as e:
        log.error("Error initializing class " + path)
        raise e


def get_static_method(full_method_name):
    try:
        spl = full_method_name.split(".")
        method_name = spl.pop()
        class_name = ".".join(spl)
        clz = get_class(class_name)
        return getattr(clz, method_name)
    except Exception as e:
        log.error("Error getting static method {} : {}".format(full_method_name, e))
        raise e


def instantiate(config, *args, **kwargs):
    assert config is not None, "Input config is None"
    try:
        clazz = get_class(config["class"])
        params = config.params if "params" in config else OmegaConf.create()
        params.merge_with(OmegaConf.create(kwargs))
        return clazz(*args, **params)
    except Exception as e:
        log.error("Error instantiating {} : {}".format(config["class"], e))
        raise e


def get_original_cwd():
    return HydraConfig().hydra.runtime.cwd


def get_relative_path(path):
    """
    converts the specified path to be relative to the original working directory the job was executed from
    if it's relative. does not change the path if it's absolute.
    :param path:
    :return:
    """
    path = Path(path)
    if path.is_absolute():
        ret = path
    else:
        ret = Path(get_original_cwd()) / path
    return str(ret)
