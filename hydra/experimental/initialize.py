# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import os
from typing import Any, Optional

from hydra._internal.hydra import Hydra
from hydra._internal.utils import (
    create_config_search_path,
    detect_calling_file_or_module_from_stack_frame,
    detect_task_name,
)
from hydra.core.global_hydra import GlobalHydra
from hydra.core.singleton import Singleton
from hydra.errors import HydraException


def get_gh_backup() -> Any:
    if GlobalHydra in Singleton._instances:
        return copy.deepcopy(Singleton._instances[GlobalHydra])
    else:
        return None


def restore_gh_from_backup(_gh_backup: Any) -> Any:
    if _gh_backup is None:
        del Singleton._instances[GlobalHydra]
    else:
        Singleton._instances[GlobalHydra] = _gh_backup


class initialize:
    """
    Initializes Hydra and add the config_path to the config search path.
    config_path is relative to the parent of the caller.
    Hydra detects the caller type automatically at runtime.

    Supported callers:
    - Python scripts
    - Python modules
    - Unit tests
    - Jupyter notebooks.
    :param config_path: path relative to the parent of the caller
    :param job_name: the value for hydra.job.name (By default it is automatically detected based on the caller)
    :param strict: (Deprecated), will be removed in the next major version
    :param caller_stack_depth: stack depth of the caller, defaults to 1 (direct caller).
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        job_name: Optional[str] = None,
        strict: Optional[bool] = None,
        caller_stack_depth: int = 1,
    ) -> None:
        self._gh_backup = get_gh_backup()

        if config_path is not None and os.path.isabs(config_path):
            raise HydraException("config_path in initialize() must be relative")
        calling_file, calling_module = detect_calling_file_or_module_from_stack_frame(
            caller_stack_depth + 1
        )
        if job_name is None:
            job_name = detect_task_name(
                calling_file=calling_file, calling_module=calling_module
            )

        Hydra.create_main_hydra_file_or_module(
            calling_file=calling_file,
            calling_module=calling_module,
            config_path=config_path,
            job_name=job_name,
            strict=strict,
        )

    def __enter__(self, *args: Any, **kwargs: Any) -> None:
        ...

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        restore_gh_from_backup(self._gh_backup)

    def __repr__(self) -> str:
        return "hydra.experimental.initialize()"


class initialize_config_module:
    """
    Initializes Hydra and add the config_module to the config search path.
    The config module must be importable (an __init__.py must exist at its top level)
    :param config_module: absolute module name, for example "foo.bar.conf".
    :param job_name: the value for hydra.job.name (default is 'app')
    """

    def __init__(self, config_module: str, job_name: str = "app"):
        self._gh_backup = get_gh_backup()

        Hydra.create_main_hydra_file_or_module(
            calling_file=None,
            calling_module=f"{config_module}.{job_name}",
            config_path=None,
            job_name=job_name,
            strict=None,
        )

    def __enter__(self, *args: Any, **kwargs: Any) -> None:
        ...

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        restore_gh_from_backup(self._gh_backup)

    def __repr__(self) -> str:
        return "hydra.experimental.initialize_config_module()"


class initialize_config_dir:
    """
    Initializes Hydra and add an absolute config dir to the to the config search path.
    The config_dir is always a path on the file system and is must be an absolute path.
    Relative paths will result in an error.
    :param config_dir: absolute file system path
    :param job_name: the value for hydra.job.name (default is 'app')
    """

    def __init__(self, config_dir: str, job_name: str = "app") -> None:
        self._gh_backup = get_gh_backup()
        # Relative here would be interpreted as relative to cwd, which - depending on when it run
        # may have unexpected meaning. best to force an absolute path to avoid confusion.
        # Can consider using hydra.utils.to_absolute_path() to convert it at a future point if there is demand.
        if not os.path.isabs(config_dir):
            raise HydraException(
                "initialize_config_dir() requires an absolute config_dir as input"
            )
        csp = create_config_search_path(search_path_dir=config_dir)
        Hydra.create_main_hydra2(
            task_name=job_name, config_search_path=csp, strict=None
        )

    def __enter__(self, *args: Any, **kwargs: Any) -> None:
        ...

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        restore_gh_from_backup(self._gh_backup)

    def __repr__(self) -> str:
        return "hydra.experimental.initialize_config_dir()"
