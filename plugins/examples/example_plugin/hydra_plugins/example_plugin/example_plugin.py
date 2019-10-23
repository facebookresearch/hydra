# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from hydra.plugins import Plugin


class ExamplePlugin(Plugin):
    def __init__(self, v):
        self.v = v

    def add(self, x):
        return self.v + x
