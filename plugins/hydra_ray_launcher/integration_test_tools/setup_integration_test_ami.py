# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import subprocess
import sys
from datetime import datetime
from typing import List

log = logging.getLogger(__name__)

dependencies = [
    "boto3==1.22.6",
    "hydra-core>=1.1.2",
    "ray[default]==1.13",
    # https://github.com/aio-libs/aiohttp/issues/6203
    "aiohttp==3.8.1",
    "cloudpickle==2.0.0",
    "pickle5==0.0.11; python_version < '3.8'",
]


def _run_command(args: List[str]) -> str:
    print(f"{str( datetime.now() )} - OUT: {args}")
    try:
        output = subprocess.check_output(args, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        log.exception(
            f"cmd: {e.cmd}"
            + f"\n\nreturncode: {e.returncode}"
            + f"\n\nstdout: {e.stdout}"
            + f"\n\nstderr: {e.stderr}"
        )
        raise
    print(f"{str( datetime.now() )} - OUT: {output}")
    return output


def run(py_version):

    _run_command(["rm", "/home/ubuntu/ray_bootstrap_config.yaml"])

    _run_command(
        ["conda", "create", "-n", f"hydra_{py_version}", f"python={py_version}", "-y"]
    )
    pip_path = f"/home/ubuntu/anaconda3/envs/hydra_{py_version}/bin/pip"
    for d in dependencies:
        _run_command([pip_path, "install", d])


if __name__ == "__main__":
    run(sys.argv[1])
