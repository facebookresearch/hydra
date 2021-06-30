# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import warnings


def deprecation_warning(message: str, stacklevel: int = 1) -> None:
    warnings.warn(message, stacklevel=stacklevel + 1)
