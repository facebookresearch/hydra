import requests
import os

os.environ['CIRCLECI_TOKEN'] = "87c43392dbf2fa64d10c3d35d2c933ba94694e68"

auth = os.environ.get("CIRCLECI_TOKEN", "0")

def run():
    r = requests.post("https://circleci.com/api/v2/project/gh/facebookresearch/hydra/pipeline", headers={"Circle-Token": auth}, data={"branch": "master"})
    print(r.json())
    r = requests.get("https://circleci.com/api/v2/me", headers={"Circle-Token": auth})
    print(r.json())


if __name__ == '__main__':
    run()