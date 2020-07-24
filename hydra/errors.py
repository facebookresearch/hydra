# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Optional, Sequence


class HydraException(Exception):
    ...


# Compact exceptions are printed in a user friendly way when they
# are intercepted by @hydra.main()
class CompactHydraException(HydraException):
    ...


class InstantiateException(CompactHydraException):
    ...


class OverrideParseException(CompactHydraException):
    def __init__(self, override: str, message: str) -> None:
        super(OverrideParseException, self).__init__(message)
        self.override = override
        self.message = message


class ConfigCompositionException(CompactHydraException):
    ...


class MissingConfigException(IOError, ConfigCompositionException):
    def __init__(
        self,
        message: str,
        missing_cfg_file: Optional[str],
        options: Optional[Sequence[str]] = None,
    ) -> None:
        super(MissingConfigException, self).__init__(message)
        self.missing_cfg_file = missing_cfg_file
        self.options = options
