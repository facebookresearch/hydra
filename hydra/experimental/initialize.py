# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Optional

from hydra.initialize import _UNSPECIFIED_


class initialize:
    def __init__(
        self,
        config_path: Optional[str] = _UNSPECIFIED_,
        job_name: Optional[str] = None,
        caller_stack_depth: int = 1,
    ) -> None:
        message = (
            "hydra.experimental.initialize() is no longer experimental. "
            "Use hydra.initialize()"
        )
        raise ImportError(message)

    def __repr__(self) -> str:
        return "hydra.experimental.initialize()"


class initialize_config_module:
    """
    Initializes Hydra and add the config_module to the config search path.
    The config module must be importable (an __init__.py must exist at its top level)
    :param config_module: absolute module name, for example "foo.bar.conf".
    :param job_name: the value for hydra.job.name (default is 'app')
    """

    def __init__(self, config_module: str, job_name: str = "app") -> None:
        message = (
            "hydra.experimental.initialize_config_module() is no longer experimental. "
            "Use hydra.initialize_config_module()."
        )
        raise ImportError(message)

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
        message = (
            "hydra.experimental.initialize_config_dir() is no longer experimental. "
            "Use hydra.initialize_config_dir()."
        )
        raise ImportError(message)

    def __repr__(self) -> str:
        return "hydra.experimental.initialize_config_dir()"
