import json
import re
import sys

import requests
import os

auth = os.environ.get("CIRCLECI_TOKEN", "0")

git_repo_pattern = "((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(/)?"

def run(branch: str, git_repo: str) -> None:
    assert auth != "0"
    p = re.compile(git_repo_pattern)
    m = re.search(p, git_repo)
    repo_name = m.group(m.groups().index(".git"))
    headers = {"Circle-Token": auth, 'Content-type': 'application/json'}
    data = {"branch": branch, "parameters": {"plugin": "hydra_colorlog", "plugin_test": True}}
    r = requests.post(f"https://circleci.com/api/v2/project/gh/{repo_name}/pipeline", headers=headers, data=json.dumps(data))
    print(r.json())



if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])