# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
import json
import os
from os.path import dirname
import re
import sys
from typing import List, Dict

import requests


auth = os.environ.get("CIRCLECI_TOKEN", "0")

git_repo_pattern = (
    "((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(/)?"
)

BASE = dirname(os.path.abspath(os.path.dirname(__file__)))

def get_available_plugin() -> List[Dict[str, str]]:
    blacklist = [".isort.cfg"]
    example_plugins = [
        {"dir_name": x, "path": f"examples/{x}"}
        for x in sorted(os.listdir(os.path.join(BASE, "plugins/examples")))
        if x not in blacklist
    ]
    plugins = [
        {"dir_name": x, "path": x}
        for x in sorted(os.listdir(os.path.join(BASE, "plugins")))
        if x != "examples"
        if x not in blacklist
    ]
    return plugins + example_plugins


def run(branch: str, git_repo: str) -> None:
    assert auth != "0"
    p = re.compile(git_repo_pattern)
    m = re.search(p, git_repo)
    repo_name = m.group(m.groups().index(".git"))
    headers = {"Circle-Token": auth, "Content-type": "application/json"}
    plugins = [p["path"] for p in get_available_plugin()]
    for p in plugins:
        data = {"branch": branch, "parameters": {"plugin": p, "plugin_test": True}}
        r = requests.post(
            f"https://circleci.com/api/v2/project/gh/{repo_name}/pipeline",
            headers=headers,
            data=json.dumps(data),
        )
        print(f"Trigger pipeline for plugin {p}, response: {r.json()}")


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
