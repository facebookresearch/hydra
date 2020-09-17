# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
import json
import os
import random
import re
from itertools import islice
from os.path import dirname
from typing import List

import requests

git_repo_pattern = (
    r"((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(/)?"
)

BASE = dirname(dirname(os.path.abspath(os.path.dirname(__file__))))


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


def get_available_plugin() -> List[str]:
    blacklist = [".isort.cfg"]
    ps = [
        {"dir_name": x, "path": x}
        for x in sorted(os.listdir(os.path.join(BASE, "plugins")))
        if x not in blacklist
    ]
    plugins = [p["path"] for p in ps]
    random.shuffle(plugins)
    return [",".join(w) for w in list(chunk(plugins, 4))]


def run() -> None:
    auth = os.environ.get("CIRCLECI_TOKEN", "0")
    branch = os.environ.get("CIRCLE_BRANCH", "")
    repo_url = os.environ.get("CIRCLE_REPOSITORY_URL", "")
    assert auth != "0", "Please set CIRCLECI_TOKEN for your project."
    p = re.compile(git_repo_pattern)
    m = re.search(p, repo_url)
    repo_name = m.group(m.groups().index(".git"))
    headers = {"Circle-Token": auth, "Content-type": "application/json"}

    for p in get_available_plugin():
        data = {"branch": branch, "parameters": {"plugin": p, "plugin_test": True}}
        post_url = f"https://circleci.com/api/v2/project/gh/{repo_name}/pipeline"
        print(f"Data: {data}")
        print(f"URL: {post_url}")
        r = requests.post(
            post_url,
            headers=headers,
            data=json.dumps(data),
        )
        assert (
            r.status_code == 201
        ), f"Unexpected response while submitting CIRCLECI job for plugins. Response: {r.json()}"
        print(f"Trigger pipeline for plugin {p}, response: {r.json()}")


if __name__ == "__main__":
    run()
