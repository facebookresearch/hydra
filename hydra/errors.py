# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Optional, Sequence


class HydraException(Exception):
    ...


class MissingConfigException(IOError, HydraException):
    def __init__(
        self,
        message: str,
        missing_cfg_file: Optional[str],
        options: Optional[Sequence[str]] = None,
    ) -> None:
        super(MissingConfigException, self).__init__(message)
        self.missing_cfg_file = missing_cfg_file
        self.options = options
