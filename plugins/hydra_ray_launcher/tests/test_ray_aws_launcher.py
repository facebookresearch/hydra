# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import hashlib
import os
import random
import string
import subprocess
import sys
import tempfile
from os.path import dirname
from pathlib import Path
from typing import List, Optional

import pytest
from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.test_utils.launcher_common_tests import (
    IntegrationTestSuite,
    LauncherTestSuite,
)
from hydra.test_utils.test_utils import chdir_plugin_root

from hydra_plugins.hydra_ray_launcher._launcher_util import (
    ray_down,
    ray_new_dir,
    ray_rsync_up,
    ray_up,
)
from hydra_plugins.hydra_ray_launcher.ray_aws_launcher import RayAWSLauncher
from plugins.hydra_ray_launcher.hydra_plugins.hydra_ray_launcher._launcher_util import (
    _run_command,
)




chdir_plugin_root()


temp_remote_dir = "/tmp/hydra_test/"
temp_remote_wheel_dir = "/tmp/wheels/"
cluster_name = "IntegrationTest-" + "".join(
    "8dSrf",
     # [random.choice(string.ascii_letters + string.digits) for n in range(5)]
)
sweep_dir = "tmp_pytest_dir"
win_msg = "Ray doesn't support Windows."
instance_role = os.environ.get("INSTANCE_ROLE_ARN", "")
cur_py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
ami = os.environ.get("AWS_RAY_AMI", "")
security_group_id = os.environ.get( "AWS_RAY_SECURITY_GROUP", "" )

ray_nodes_conf = {
    "InstanceType": "m5.large",
    "ImageId": ami,
    "SubnetId": "subnet-acd2cfe7",
    "SecurityGroupIds": [security_group_id],
    "IamInstanceProfile": {"Arn" : instance_role}
}

ray_nodes_conf_override = str(ray_nodes_conf).replace("'", "").replace(" ", "")

# base is hydra/plugins/
BASE = Path(dirname(dirname(os.path.abspath(os.path.dirname(__file__)))))


def build_installed_plugin_wheels(tmpdir: str) -> List[str]:
    """
    This  only works on ray launcher plugin wheels for now, reasons being in our base AMI
    we do not necessarily have the dependency for other plugins.
    """
    command = "python -m pip --disable-pip-version-check list | grep hydra | grep -v hydra-core "
    output = subprocess.getoutput(command).split("\n")
    plugins_path = [x.split()[0].replace("-", "_") for x in output]
    wheels = []
    for p in plugins_path:
        wheel = build_plugin_wheel(p, Path(tmpdir))
        wheels.append(wheel)
    assert len(wheels) == 1 and "hydra_ray_launcher" in wheels[0], "Other plugins installed may cause tests failure."
    return wheels


def build_plugin_wheel(plugin: str, tmp_wheel_dir: str) -> str:
    os.chdir(BASE / plugin)
    print(f"Build wheel for {plugin}, save wheel to {tmp_wheel_dir}.")
    subprocess.check_output(
        f"python setup.py sdist bdist_wheel && cp dist/*.whl {tmp_wheel_dir}",
        shell=True,
    )
    wheel = subprocess.getoutput("ls dist/*.whl").split("/")[-1]
    os.chdir(BASE)
    return wheel


def build_core_wheel(tmp_wheel_dir: str) -> str:
    os.chdir(dirname(BASE))
    subprocess.check_output(
        f"python setup.py sdist bdist_wheel && cp dist/*.whl {tmp_wheel_dir}",
        shell=True,
    )
    wheel = subprocess.getoutput("ls dist/*.whl").split("/")[-1]
    os.chdir(BASE)
    return wheel


def download_ray_wheel(tmp_wheel_dir: str) -> str:
    # release sha picked from the top commit from ray release branch
    # hardcode for now, it'd be great to automate this.
    release_sha = {"0.8.7": "89fd21ff610f237691908997d12fa9ee465e68d4"}
    # first grep local ray version
    ray_version = subprocess.getoutput("pip freeze | grep ray==").split("==")[1]
    if ray_version not in release_sha.keys():
        raise ValueError(f"Do not have commit sha for ray {ray_version}")
    current_os = "linux"
    bucket_path = (
        f"s3://ray-wheels/releases/{ray_version}/{release_sha.get(ray_version)}/"
    )
    pyversion = str(sys.version_info.major) + str(sys.version_info.minor)
    output = subprocess.getoutput(
        f"aws s3 ls {bucket_path} | grep cp{pyversion} | grep {current_os}"
    )
    wheels = output.split("\n")
    assert (
        len(wheels) == 1
    ), f"Found {len(wheels)} number of wheels instead of exactly 1"
    wheel = wheels[0].split()[-1]

    # download the wheels
    os.chdir(str(tmp_wheel_dir))
    object_url = f"https://ray-wheels.s3-us-west-2.amazonaws.com/releases/{ray_version}/{release_sha.get(ray_version)}/{wheel}"
    command = f"wget {object_url}"
    print(f"Saving ray wheel in {tmp_wheel_dir}, Command: {command}")
    subprocess.check_output(command, shell=True)
    os.chdir(BASE)
    return wheel


def upload_and_install_wheels(
    tmp_wheel_dir: str,
    yaml: str,
    core_wheel: str,
    ray_wheel: str,
    plugin_wheels: List[str],
) -> None:

    ray_rsync_up(yaml, tmp_wheel_dir + "/", temp_remote_wheel_dir)
    print(f"Install hydra-core wheel {core_wheel}")
    out, err = _run_command(
        [
            "ray",
            "exec",
            yaml,
            f"pip install {temp_remote_wheel_dir}{core_wheel}",
        ]
    )
    print(f"OUT: {out}")
    print(f"ERR: {err}")

    print(f"Install ray wheel {ray_wheel}")
    out, err = _run_command(
        [
            "ray",
            "exec",
            yaml,
            f"pip install {temp_remote_wheel_dir}{ray_wheel}",
        ]
    )
    print(f"OUT: {out}")
    print(f"ERR: {err}")

    for p in plugin_wheels:
        print(f"Install ray wheel {p}")
        out, err = _run_command(
            [
                "ray",
                "exec",
                yaml,
                f"pip install {temp_remote_wheel_dir}{p}",
            ]
        )
        print(f"OUT: {out}")
        print(f"ERR: {err}")


def get_requirements_sha() -> str:
    requirements_path = Path(dirname(dirname(dirname(os.path.abspath(dirname(__file__))))))/"requirements/requirements.txt"
    with open(requirements_path, "rb") as f:
        # read contents of the file
        data = f.read()
        # pipe contents of the file through
        return hashlib.md5(data).hexdigest()


@pytest.mark.skipif(sys.platform.startswith("win"), reason=win_msg)  # type: ignore
def test_discovery() -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking for Launchers
    assert RayAWSLauncher.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Launcher)
    ]


@pytest.fixture(scope="module")
def manage_cluster() -> str:
    # first assert the SHA of requirments haven't changed
    # if changed, means we need to update test AMI.
    assert get_requirements_sha() == "9975198e6a955d91d823b226d88ccd48", "hydra-core requirements changed"

    assert instance_role != "", "Please set INSTANCE_ROLE for the test."


    print("OVERRIDE")
    print(f"hydra.launcher.ray_cluster_cfg.head_node=\'{ray_nodes_conf_override}\'")

    # test only need cluster name and provider info for connection.
    connect_yaml = f"""
cluster_name: {cluster_name}
provider:
  type: aws
  region: us-west-2
  availability_zone: us-west-2a,us-west-2b
  cache_stopped_nodes: False
  key_pair:
     key_name: hydra_test_{cluster_name}
auth:
  ssh_user: ubuntu
setup_commands:
  - echo 'export PATH="$HOME/anaconda3/envs/hydra_{cur_py_version}/bin:$PATH"' >> ~/.bashrc
head_setup_commands: []
head_node:
  ImageId: {ami}
  SubnetId: subnet-acd2cfe7
  InstanceType: m5.large
  SecurityGroupIds:
  - sg-06a39fb434733da79
  IamInstanceProfile:
    Arn: {instance_role}
worker_nodes:
  ImageId: {ami}
  SubnetId: subnet-acd2cfe7
  InstanceType: m5.large
  SecurityGroupIds:
  - sg-06a39fb434733da79
  IamInstanceProfile:
    Arn: {instance_role}
    """
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
        with open(f.name, "w") as file:
            print(connect_yaml, file=file)
        temp_yaml = f.name
        ray_up(temp_yaml)
        print(f"DONE ray up")
        ray_new_dir(temp_yaml, temp_remote_dir, False)
        ray_new_dir(temp_yaml, temp_remote_wheel_dir, False)

        # build all the wheels
        tmpdir = tempfile.mkdtemp()
        plugin_wheels = build_installed_plugin_wheels(tmpdir)
        core_wheel = build_core_wheel(tmpdir)
        ray_wheel = download_ray_wheel(tmpdir)
        upload_and_install_wheels(
            tmpdir, temp_yaml, core_wheel, ray_wheel, plugin_wheels
        )
        yield
        # ray_down(f.name)


@pytest.mark.skipif(sys.platform.startswith("win"), reason=win_msg)
@pytest.mark.usefixtures("manage_cluster")
@pytest.mark.parametrize(
    "launcher_name, overrides, tmpdir",
    [
        (
            "ray_aws",
            [
                f"hydra.launcher.ray_cluster_cfg.cluster_name={cluster_name}",
                "hydra.launcher.stop_cluster=False",
                f"hydra.launcher.sync_down.source_dir={sweep_dir}/",
                f"hydra.launcher.sync_down.target_dir={sweep_dir}",
                f"hydra.launcher.ray_cluster_cfg.provider.key_pair.key_name=hydra_test_{cluster_name}",
                # f"'hydra.launcher.ray_cluster_cfg.head_node={ray_nodes_conf_override}'",
                f'+hydra.launcher.ray_cluster_cfg.worker_nodes={ray_nodes_conf_override}',
                f'+hydra.launcher.ray_cluster_cfg.head_node={ray_nodes_conf_override}',
            ],
            Path(sweep_dir),
        )
    ],
)
class TestRayAWSLauncher(LauncherTestSuite):
    pass


# @pytest.mark.skipif(sys.platform.startswith("win"), reason=win_msg)
# @pytest.mark.usefixtures("manage_cluster")
# @pytest.mark.parametrize(
#     "tmpdir,  task_launcher_cfg, extra_flags",
#     [
#         (
#             Path(temp_remote_dir),
#             {
#                 "defaults": [
#                     {"hydra/launcher": "ray_aws"},
#                     {"hydra/hydra_logging": "hydra_debug"},
#                     {"hydra/job_logging": "disabled"},
#                 ]
#             },
#             [
#                 "-m",
#                 f"hydra.launcher.ray_cluster_cfg.cluster_name={cluster_name}",
#                 "hydra.launcher.stop_cluster=False",
#                 f"hydra.launcher.sync_down.source_dir={temp_remote_dir}/",
#                 f"hydra.launcher.sync_down.target_dir={temp_remote_dir}",
#                 f"hydra.launcher.ray_cluster_cfg.provider.key_pair.key_name=hydra_test_{cluster_name}",
#                 f"hydra.launcher.ray_cluster_cfg.head_node=\'{ray_nodes_conf_override}\'",
#                 f"hydra.launcher.ray_cluster_cfg.worker_nodes=\'{ray_nodes_conf_override}\'",
#             ],
#         )
#     ],
# )
# class TestRayAWSLauncherIntegration(IntegrationTestSuite):
#     """
#     Run this launcher through the integration test suite.
#     """
#
#     def get_test_app_working_dir(self) -> Optional[Path]:
#         """
#         By default test applications working dir is tmpdir, override this method if that's not the case.
#         This could be helpful when the tests kick off applications on remote machines.
#         """
#         return Path("/home/ubuntu")
