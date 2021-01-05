# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import subprocess
import sys
from datetime import datetime

dependencies = [
    "boto3==1.16.48",
    "hydra-core>=1.0.0",
    "ray==1.1.0",
    "cloudpickle==1.6.0",
    "pickle5==0.0.11",
]


def _run_command(command: str) -> str:
    print(f"{str( datetime.now() )} - OUT: {command}")
    output = subprocess.getoutput(command)
    print(f"{str( datetime.now() )} - OUT: {output}")
    return output


def run(py_version):

    _run_command("rm /home/ubuntu/ray_bootstrap_config.yaml")

    _run_command(f"conda create -n hydra_{py_version} python={py_version} -y")
    pip_path = f"/home/ubuntu/anaconda3/envs/hydra_{py_version}/bin/pip"
    for d in dependencies:
        _run_command(f"{pip_path} install {d}")


if __name__ == "__main__":
    run(sys.argv[1])
