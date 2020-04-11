# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
from pathlib import Path

from hydra.plugins.plugin import Plugin

if "TMP_FILE" in os.environ:
    with Path(os.environ["TMP_FILE"]).open(mode="a") as f:
        f.write("imported\n")


class DiscoveryTestPlugin(Plugin):
    ...
