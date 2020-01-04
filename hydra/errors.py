# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Sequence


class MissingConfigException(IOError):
    def __init__(
        self, message: str, missing_cfg_file: str, options: Sequence[str] = []
    ) -> None:
        super(MissingConfigException, self).__init__(message)
        self.missing_cfg_file = missing_cfg_file
        self.options = options
