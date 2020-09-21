# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import random
import string
import sys
import tempfile
from pathlib import Path
from typing import Optional, List

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

chdir_plugin_root()


temp_remote_dir = "/tmp/hydra_test/"
cluster_name = "IntegrationTest-" + "".join(
    [random.choice(string.ascii_letters + string.digits) for n in range(5)]
)
sweep_dir = "tmp_pytest_dir"
win_msg = "Ray doesn't support Windows."
instance_role = os.environ.get("INSTANCE_ROLE_ARN", "")

temp_local_wheels_dir = ""

def get_all_plugins() -> List[str]:
    plugins = os.environ.get( "PLUGINS", "ALL" ).split( "," )
    if "ALL" in plugins:


def build_wheel(plugin: str) -> str:


def upload_wheel() -> str:



@pytest.mark.skipif(sys.platform.startswith("win"), reason=win_msg)  # type: ignore
def test_discovery() -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking for Launchers
    assert RayAWSLauncher.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Launcher)
    ]


@pytest.fixture(scope="module")
def manage_cluster() -> str:
    assert instance_role != "", "Please set INSTANCE_ROLE for the test."
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
head_node:
  InstanceType: m5.large
  ImageId: ami-008d8ed4bd7dc2485
  IamInstanceProfile: 
      Arn: {instance_role}
    """
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
        with open(f.name, "w") as file:
            print(connect_yaml, file=file)
        temp_yaml = f.name
        ray_up(temp_yaml)
        ray_new_dir(temp_yaml, temp_remote_dir, False)
        yield
        ray_down(f.name)


@pytest.mark.skipif(sys.platform.startswith("win"), reason=win_msg)
@pytest.mark.usefixtures("manage_cluster")
@pytest.mark.parametrize(
    "launcher_name, overrides, tmpdir",
    [
        (
            "ray_aws",
            [
                f"hydra.launcher.params.ray_cluster_cfg.cluster_name={cluster_name}",
                "hydra.launcher.params.stop_cluster=False",
                f"hydra.launcher.params.sync_down.source_dir={sweep_dir}/",
                f"hydra.launcher.params.sync_down.target_dir={sweep_dir}",
                f"hydra.launcher.params.ray_cluster_cfg.provider.key_pair.key_name=hydra_test_{cluster_name}",
            ],
            Path(sweep_dir),
        )
    ],
)
class TestRayAWSLauncher(LauncherTestSuite):
    pass


@pytest.mark.skipif(sys.platform.startswith("win"), reason=win_msg)
@pytest.mark.usefixtures("manage_cluster")
@pytest.mark.parametrize(
    "tmpdir,  task_launcher_cfg, extra_flags",
    [
        (
            Path(temp_remote_dir),
            {
                "defaults": [
                    {"hydra/launcher": "ray_aws"},
                    {"hydra/hydra_logging": "hydra_debug"},
                    {"hydra/job_logging": "disabled"},
                ]
            },
            [
                "-m",
                f"hydra.launcher.params.ray_cluster_cfg.cluster_name={cluster_name}",
                "hydra.launcher.params.stop_cluster=False",
                f"hydra.launcher.params.sync_down.source_dir={temp_remote_dir}/",
                f"hydra.launcher.params.sync_down.target_dir={temp_remote_dir}",
                f"hydra.launcher.params.ray_cluster_cfg.provider.key_pair.key_name=hydra_test_{cluster_name}",
                f"hydra.launcher.params.ray_cluster_cfg.provider.key_pair.key_name=hydra_test_{cluster_name}",
            ],
        )
    ],
)
class TestRayAWSLauncherIntegration(IntegrationTestSuite):
    """
    Run this launcher through the integration test suite.
    """

    def get_test_app_working_dir(self) -> Optional[Path]:
        """
        By default test applications working dir is tmpdir, override this method if that's not the case.
        This could be helpful when the tests kick off applications on remote machines.
        """
        return Path("/home/ubuntu")
