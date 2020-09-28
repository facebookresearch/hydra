# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import subprocess
from datetime import datetime


def _run_command(command: str) -> str:
    print(f"{str( datetime.now() )} - OUT: {command}")
    output = subprocess.getoutput(command)
    print(f"{str( datetime.now() )} - OUT: {output}")
    return output


def run():
    output = _run_command("conda search python").split("\n")

    # gather all the python versions and install conda envs
    versions = set()
    for o in output:
        o = o.split()
        if len(o) > 2 and o[0] == "python" and float(o[1][:3]) >= 3.6:
            versions.add(o[1])
    print(sorted(versions))

    _run_command("rm /home/ubuntu/ray_bootstrap_config.yaml")

    # prep conda env for all python versions

    for v in sorted(versions):
        _run_command(f"conda create -n hydra_{v} python={v} -y")
        pip_path = f"/home/ubuntu/anaconda3/envs/hydra_{v}/bin/pip"
        _run_command(f"{pip_path} install ray")
        _run_command(f"{pip_path} install boto3==1.15.6")
        _run_command(f"{pip_path} install importlib-resources")
        _run_command(f"{pip_path} install omegaconf==2.0.2")
        _run_command(f"{pip_path} install antlr4-python3-runtime==4.8")
        _run_command(f"{pip_path} install --ignore-installed PyYAML")


if __name__ == "__main__":
    run()
