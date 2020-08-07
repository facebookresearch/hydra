# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
import json
import os
import re
import sys
from os.path import dirname
from typing import List

import requests

auth = os.environ.get("CIRCLECI_TOKEN", "0")

git_repo_pattern = (
    r"((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(/)?"
)

BASE = dirname(os.path.abspath(os.path.dirname(__file__)))


def get_available_plugin() -> List[str]:
    blacklist = [".isort.cfg"]
    ps = [
        {"dir_name": x, "path": x}
        for x in sorted(os.listdir(os.path.join(BASE, "plugins")))
        if x != "examples"
        if x not in blacklist
    ]
    return [p["path"] for p in ps] + ["examples"]


def run(branch: str, git_repo: str) -> None:
    assert auth != "0"
    p = re.compile(git_repo_pattern)
    m = re.search(p, git_repo)
    repo_name = m.group(m.groups().index(".git"))
    headers = {"Circle-Token": auth, "Content-type": "application/json"}

    for p in get_available_plugin():
        data = {"branch": branch, "parameters": {"plugin": p, "plugin_test": True}}
        r = requests.post(
            f"https://circleci.com/api/v2/project/gh/{repo_name}/pipeline",
            headers=headers,
            data=json.dumps(data),
        )
        print(f"Trigger pipeline for plugin {p}, response: {r.json()}")


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
