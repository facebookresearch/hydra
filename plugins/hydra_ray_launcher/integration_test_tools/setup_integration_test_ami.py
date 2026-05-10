# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import subprocess
import sys
from datetime import datetime
from shlex import quote

dependencies = [
    "boto3",
    "hydra-core>=1.1.2",
    "ray[default]<3",
    "aiohttp<4",
    "cloudpickle<3",
]


def _run_command(command: str) -> str:
    print(f"{str( datetime.now() )} - OUT: {command}")
    output = subprocess.getoutput(command)  # nosec B605
    print(f"{str( datetime.now() )} - OUT: {output}")
    return output


def run(py_version):
    _run_command("rm /home/ubuntu/ray_bootstrap_config.yaml")

    _run_command(f"conda create -n hydra_{py_version} python={py_version} -y")
    pip_path = f"/home/ubuntu/anaconda3/envs/hydra_{py_version}/bin/pip"
    for d in dependencies:
        _run_command(f"{pip_path} install {quote(d)}")


if __name__ == "__main__":
    run(sys.argv[1])
