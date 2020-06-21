# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import os
from contextlib import contextmanager
from typing import Any, Optional

from hydra._internal.hydra import Hydra
from hydra._internal.utils import detect_calling_file_or_module_from_stack_frame
from hydra.core.global_hydra import GlobalHydra
from hydra.errors import HydraException


def initialize(
    config_path: Optional[str],
    job_name: Optional[str] = None,
    strict: Optional[bool] = None,
    caller_stack_depth: int = 1,
) -> None:
    """
    Initializes Hydra and add the config_path to the config search path.
    config_path is relative to the parent of the caller.
    Hydra detects the caller type automatically at runtime.
    In addition, Hydra uses the name of the detected caller as the hydra.job.name.
    Supported callers:
    - Python scripts
    - Python modules
    - Unit tests
    - Jupyter notebooks.
    :param config_path: path relative to the caller
    :param job_name: Optional job name to use instead of the automatically detected one
    :param strict: (Deprecated), will be removed in the next major version
    :param caller_stack_depth: stack depth of the caller, defaults to 1 (direct caller).
    """
    calling_file, calling_module = detect_calling_file_or_module_from_stack_frame(
        caller_stack_depth + 1
    )
    Hydra.create_main_hydra_file_or_module(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path=config_path,
        job_name=job_name,
        strict=strict,
    )


def initialize_config_module(config_module: str, job_name: str = "app") -> None:
    """
    Initializes Hydra and add the config_module to the config search path.
    The config module must be importable (an __init__.py must exist at its top level)
    :param config_module: absolute module name, for example "foo.bar.conf".
    :param job_name: the value for hydra.job.name (default is 'app')
    """
    Hydra.create_main_hydra_file_or_module(
        calling_file=None,
        calling_module=f"{config_module}.{job_name}",
        config_path=None,
        job_name=job_name,
        strict=None,
    )


def initialize_config_dir(
    config_dir: str, job_name: Optional[str] = None, caller_stack_depth: int = 1,
) -> None:
    """
    Initializes Hydra and add the config_path to the config search path.
    The config_path is always a path on the file system.
    The config_path can either be an absolute path on the file system or a file relative to the caller.
    Supported callers:
    - Python scripts
    - Unit tests
    - Jupyter notebooks.
    If the caller is a Python module and the config dir is relative an error will be raised.
    :param config_dir: file system path relative to the caller or absolute
    :param job_name: Optional job name to use instead of the automatically detected one
    :param caller_stack_depth: stack depth of the caller, defaults to 1 (direct caller).
    """
    calling_file, calling_module = detect_calling_file_or_module_from_stack_frame(
        caller_stack_depth + 1
    )
    if calling_module is not None and os.path.isabs(config_dir):
        raise HydraException(
            "initialize_config_dir does not support a module caller with a relative config_dir"
        )
    Hydra.create_main_hydra_file_or_module(
        calling_file=calling_file,
        calling_module=calling_module,
        config_path=config_dir,
        job_name=job_name,
        strict=None,
    )


# TODO: is it possible to have a callable that also acts as the context? can we eliminate this context?
@contextmanager
def initialize_ctx(
    config_path: str, job_name: Optional[str] = None, caller_stack_depth: int = 1
) -> Any:
    try:
        gh = copy.deepcopy(GlobalHydra.instance())
        initialize(
            config_path=config_path,
            job_name=job_name,
            caller_stack_depth=caller_stack_depth + 1,
        )
        yield
    finally:
        GlobalHydra.set_instance(gh)


@contextmanager
def initialize_config_module_ctx(config_module: str, job_name: str = "app") -> Any:
    try:
        gh = copy.deepcopy(GlobalHydra.instance())
        initialize_config_module(config_module=config_module, job_name=job_name)
        yield
    finally:
        GlobalHydra.set_instance(gh)


@contextmanager
def initialize_config_dir_ctx(
    config_dir: str, job_name: Optional[str] = None, caller_stack_depth: int = 1,
) -> Any:
    try:
        gh = copy.deepcopy(GlobalHydra.instance())
        initialize_config_dir(
            config_dir=config_dir,
            job_name=job_name,
            caller_stack_depth=caller_stack_depth + 1,
        )
        yield
    finally:
        GlobalHydra.set_instance(gh)
