# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra.plugins.plugin import Plugin


class NotHiddenTestPlugin(Plugin):
    def __init__(self, v: int) -> None:
        self.v = v
