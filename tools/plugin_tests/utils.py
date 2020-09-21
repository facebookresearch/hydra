# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
from os.path import dirname
from typing import Dict, List

BASE = dirname(dirname(os.path.abspath(os.path.dirname(__file__))))


def list_plugins_in_dir(directory: str) -> List[Dict[str, str]]:
    blacklist = [".isort.cfg", "examples"]
    return [
        {"dir_name": x, "path": x}
        for x in sorted(os.listdir(os.path.join(BASE, directory)))
        if x not in blacklist
    ]
