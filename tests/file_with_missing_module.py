# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

# Used for testing that instantiation is failing with the right error
# in case of a missing imported module
import some_missing_module  # type: ignore # noqa: F401


class AClass:
    def __init__(self) -> None:
        self.x = 1
