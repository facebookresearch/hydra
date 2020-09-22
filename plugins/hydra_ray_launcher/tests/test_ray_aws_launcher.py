# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
from os.path import dirname
import random
import string
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional, List

import boto3
from boto3 import session
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
    ray_up,
)
from hydra_plugins.hydra_ray_launcher.ray_aws_launcher import RayAWSLauncher

from plugins.hydra_ray_launcher.hydra_plugins.hydra_ray_launcher._launcher_util import _run_command

chdir_plugin_root()


temp_remote_dir = "/tmp/hydra_test/"
cluster_name = "IntegrationTest-" + "".join(
    [random.choice(string.ascii_letters + string.digits) for n in range(5)]
)
sweep_dir = "tmp_pytest_dir"
win_msg = "Ray doesn't support Windows."
instance_role = os.environ.get("INSTANCE_ROLE_ARN", "")


# base is hydra/plugins/
BASE = Path(dirname(dirname(os.path.abspath(os.path.dirname(__file__)))))

def get_ray_wheel() -> str:
    if sys.platform == "darwin":



def test_get_installed_plugins(tmpdir) -> List[str]:
    # command = "python -m pip --disable-pip-version-check list | grep hydra | grep -v hydra-core "
    # output = subprocess.getoutput(command).split("\n")
    # plugins_path = [x.split()[0].replace("-", "_") for x in output]
    # build_wheel("hydra_nevergrad_sweeper", Path(tmpdir))
    download_ray_wheel(Path(tmpdir))


def build_wheel(plugin: str, tmp_wheel_dir: Path) -> str:
    tmp_wheel_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(BASE/plugin)
    output = subprocess.check_output(f"python setup.py sdist bdist_wheel && cp dist/*.whl {tmp_wheel_dir}", shell=True)
    print(output)


def download_ray_wheel(tmp_wheel_dir: Path) -> None:
    print("TMP WHEEL DIR")
    print(tmp_wheel_dir)
    os.chdir(tmp_wheel_dir)
    subprocess.check_output("wget https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-0.9.0.dev0-cp38-cp38-manylinux1_x86_64.whl",  shell=True)
    os.chdir(BASE)

def upload_wheel() -> str:
    ...



# @pytest.mark.skipif(sys.platform.startswith("win"), reason=win_msg)  # type: ignore
# def test_discovery() -> None:
#     # Tests that this plugin can be discovered via the plugins subsystem when looking for Launchers
#     assert RayAWSLauncher.__name__ in [
#         x.__name__ for x in Plugins.instance().discover(Launcher)
#     ]
#
#
# @pytest.fixture(scope="module")
# def manage_cluster() -> str:
#     assert instance_role != "", "Please set INSTANCE_ROLE for the test."
#     # test only need cluster name and provider info for connection.
#     connect_yaml = f"""
# cluster_name: {cluster_name}
# provider:
#   type: aws
#   region: us-west-2
#   availability_zone: us-west-2a,us-west-2b
#   cache_stopped_nodes: False
#   key_pair:
#      key_name: hydra_test_{cluster_name}
# auth:
#   ssh_user: ubuntu
# head_node:
#   InstanceType: m5.large
#   ImageId: ami-008d8ed4bd7dc2485
#   IamInstanceProfile:
#       Arn: {instance_role}
#     """
#     with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
#         with open(f.name, "w") as file:
#             print(connect_yaml, file=file)
#         temp_yaml = f.name
#         ray_up(temp_yaml)
#         ray_new_dir(temp_yaml, temp_remote_dir, False)
#         yield
#         ray_down(f.name)
#
#
# @pytest.mark.skipif(sys.platform.startswith("win"), reason=win_msg)
# @pytest.mark.usefixtures("manage_cluster")
# @pytest.mark.parametrize(
#     "launcher_name, overrides, tmpdir",
#     [
#         (
#             "ray_aws",
#             [
#                 f"hydra.launcher.params.ray_cluster_cfg.cluster_name={cluster_name}",
#                 "hydra.launcher.params.stop_cluster=False",
#                 f"hydra.launcher.params.sync_down.source_dir={sweep_dir}/",
#                 f"hydra.launcher.params.sync_down.target_dir={sweep_dir}",
#                 f"hydra.launcher.params.ray_cluster_cfg.provider.key_pair.key_name=hydra_test_{cluster_name}",
#             ],
#             Path(sweep_dir),
#         )
#     ],
# )
# class TestRayAWSLauncher(LauncherTestSuite):
#     pass
#
#
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
#                 f"hydra.launcher.params.ray_cluster_cfg.cluster_name={cluster_name}",
#                 "hydra.launcher.params.stop_cluster=False",
#                 f"hydra.launcher.params.sync_down.source_dir={temp_remote_dir}/",
#                 f"hydra.launcher.params.sync_down.target_dir={temp_remote_dir}",
#                 f"hydra.launcher.params.ray_cluster_cfg.provider.key_pair.key_name=hydra_test_{cluster_name}",
#                 f"hydra.launcher.params.ray_cluster_cfg.provider.key_pair.key_name=hydra_test_{cluster_name}",
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
