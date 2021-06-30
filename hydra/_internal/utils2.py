# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import warnings


def deprecation_warning(message: str, stacklevel: int = 1) -> None:
    warnings_as_errors = os.environ.get("HYDRA_DEPRECATION_WARNINGS_AS_ERRORS", None)
    if warnings_as_errors:
        raise DeprecationWarning(message)
    else:
        warnings.warn(message, stacklevel=stacklevel + 1)
