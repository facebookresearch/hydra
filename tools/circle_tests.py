import json
import re
import sys
from typing import List

import requests
import os

from noxfile import get_available_plugin

auth = os.environ.get("CIRCLECI_TOKEN", "0")

git_repo_pattern = "((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(/)?"

def run(branch: str, git_repo: str) -> None:
    assert auth != "0"
    p = re.compile(git_repo_pattern)
    m = re.search(p, git_repo)
    repo_name = m.group(m.groups().index(".git"))
    headers = {"Circle-Token": auth, 'Content-type': 'application/json'}
    plugins = [p["path"] for p in get_available_plugin()]
    for p in plugins:
        data = {"branch": branch, "parameters": {"plugin": p, "plugin_test": True}}
        r = requests.post(f"https://circleci.com/api/v2/project/gh/{repo_name}/pipeline", headers=headers, data=json.dumps(data))
        print(f"Trigger pipeline for plugin {p}, response: {r.json()}")


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])