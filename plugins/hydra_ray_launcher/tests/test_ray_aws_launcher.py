# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import hashlib
import logging
import os
import random
import string
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Generator, List, Optional

from omegaconf import OmegaConf
import pytest
from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.test_utils.launcher_common_tests import (
    IntegrationTestSuite,
    LauncherTestSuite,
)
from hydra.test_utils.test_utils import chdir_hydra_root, chdir_plugin_root

from hydra_plugins.hydra_ray_launcher._launcher_util import (  # type: ignore
    _run_command,
    ray_down,
    ray_new_dir,
    ray_rsync_up,
    ray_up,
)
from hydra_plugins.hydra_ray_launcher.ray_aws_launcher import (  # type: ignore
    RayAWSLauncher,
)

temp_remote_dir = "/tmp/hydra_test/"  # nosec
temp_remote_wheel_dir = "/tmp/wheels/"  # nosec
sweep_dir = "tmp_pytest_dir"  # nosec

cluster_name = "IntegrationTest-" + "".join(
    [random.choice(string.ascii_letters + string.digits) for n in range(5)]
)

win_msg = "Ray doesn't support Windows."
cur_py_version = (
    f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
)
ami = os.environ.get("AWS_RAY_AMI", "")
security_group_id = os.environ.get("AWS_RAY_SECURITY_GROUP", "")
subnet_id = os.environ.get("AWS_RAY_SUBNET", "")
instance_role = os.environ.get("INSTANCE_ROLE_ARN", "")

# temporary solution. we will build customized AMI everytime the requirments changes.
ray_requirements_sha = "bdefc02ff3b9f667f37ecce9f2fc5ac6"
hydra_core_requirements_sha = "394984911320e5884cb055a5d13d7545"

assert (
    ami != "" and security_group_id != "" and subnet_id != "" and instance_role != ""
), (
    f"Missing variable for test, ami={ami}, security_group_id={security_group_id}, subnet_id={subnet_id}, "
    f"instance_role={instance_role}"
)


ray_nodes_conf = {
    "InstanceType": "m5.large",
    "ImageId": ami,
    "SubnetId": f"{subnet_id}",
    "SecurityGroupIds": [security_group_id],
    "IamInstanceProfile": {"Arn": instance_role},
}

ray_nodes_conf_override = str(ray_nodes_conf).replace("'", "").replace(" ", "")

log = logging.getLogger(__name__)

chdir_plugin_root()


def build_ray_launcher_wheel(tmpdir: str) -> List[str]:
    """
    This  only works on ray launcher plugin wheels for now, reasons being in our base AMI
    we do not necessarily have the dependency for other plugins.
    """
    command = "python -m pip --disable-pip-version-check list | grep hydra | grep -v hydra-core "
    output = subprocess.getoutput(command).split("\n")
    plugins_path = [x.split()[0].replace("-", "_") for x in output]
    assert (
        len(plugins_path) == 1 and "hydra_ray_launcher" == plugins_path[0]
    ), "Ray test AMI doesn't have dependency installed for other plugins."

    sha = get_requirements_sha("plugins/hydra_ray_launcher/setup.py")

    if sha != ray_requirements_sha:
        log.warning("Ray setup.py changed, we may need new launcher test AMI!")
    wheels = []
    for p in plugins_path:
        wheel = build_plugin_wheel(p, tmpdir)
        wheels.append(wheel)
    return wheels


def build_plugin_wheel(plugin: str, tmp_wheel_dir: str) -> str:
    os.chdir(Path("plugins") / plugin)
    log.info(f"Build wheel for {plugin}, save wheel to {tmp_wheel_dir}.")
    subprocess.getoutput(
        f"python setup.py sdist bdist_wheel && cp dist/*.whl {tmp_wheel_dir}"
    )
    wheel = subprocess.getoutput("ls dist/*.whl").split("/")[-1]
    chdir_hydra_root()
    return wheel


def build_core_wheel(tmp_wheel_dir: str) -> str:
    chdir_hydra_root()
    subprocess.getoutput(
        f"python setup.py sdist bdist_wheel && cp dist/*.whl {tmp_wheel_dir}"
    )
    wheel = subprocess.getoutput("ls dist/*.whl").split("/")[-1]
    return wheel


def upload_and_install_wheels(
    tmp_wheel_dir: str,
    yaml: str,
    core_wheel: str,
    plugin_wheels: List[str],
) -> None:
    ray_rsync_up(yaml, tmp_wheel_dir + "/", temp_remote_wheel_dir)
    log.info(f"Install hydra-core wheel {core_wheel}")
    _run_command(
        [
            "ray",
            "exec",
            yaml,
            f"pip install {temp_remote_wheel_dir}{core_wheel}",
        ]
    )

    for p in plugin_wheels:
        log.info(f"Install plugin wheel {p}")
        _run_command(
            [
                "ray",
                "exec",
                yaml,
                f"pip install {temp_remote_wheel_dir}{p}",
            ]
        )


def get_requirements_sha(path_to_hydra_root: Optional[str] = None) -> str:
    chdir_hydra_root()
    if path_to_hydra_root:
        requirements_path = Path(path_to_hydra_root)
    else:
        requirements_path = Path("requirements/requirements.txt")
    with open(requirements_path, "rb") as f:
        data = f.read()
        return hashlib.md5(data).hexdigest()  # nosec


@pytest.mark.skipif(sys.platform.startswith("win"), reason=win_msg)  # type: ignore
def test_discovery() -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking for Launchers
    assert RayAWSLauncher.__name__ in [
        x.__name__ for x in Plugins.instance().discover(Launcher)
    ]


@pytest.fixture(scope="module")  # type: ignore
def manage_cluster() -> Generator[None, None, None]:
    # first assert the SHA of requirements hasn't changed
    # if changed, means we need to update test AMI.

    if get_requirements_sha() != hydra_core_requirements_sha:
        log.warning(
            "Hydra core requirements changes. This may mean we need to update RAY test AMI."
        )

    # build all the wheels
    tmpdir = tempfile.mkdtemp()
    plugin_wheels = build_ray_launcher_wheel(tmpdir)
    core_wheel = build_core_wheel(tmpdir)
    connect_config = {
        "cluster_name": cluster_name,
        "provider": {
            "type": "aws",
            "region": "us-west-2",
            "availability_zone": "us-west-2a,us-west-2b",
            "cache_stopped_nodes": False,
            "key_pair": {"key_name": f"hydra_test_{cluster_name}"},
        },
        "auth": {"ssh_user": "ubuntu"},
        "setup_commands": [
            f"echo 'export PATH=\"$HOME/anaconda3/envs/hydra_{cur_py_version}/bin:$PATH\"' >> ~/.bashrc"
        ],
        "head_setup_commands": [],
        "head_node": ray_nodes_conf,
        "worker_nodes": ray_nodes_conf,
    }
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
        with open(f.name, "w") as file:
            OmegaConf.save(config=connect_config, f=file.name, resolve=True)
            # print(connect_yaml, file=file)
        temp_yaml = f.name
        ray_up(temp_yaml)
        ray_new_dir(temp_yaml, temp_remote_dir, False)
        ray_new_dir(temp_yaml, temp_remote_wheel_dir, False)
        upload_and_install_wheels(tmpdir, temp_yaml, core_wheel, plugin_wheels)
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
                f"hydra.launcher.ray_cluster_cfg.cluster_name={cluster_name}",
                "hydra.launcher.stop_cluster=False",
                f"hydra.launcher.sync_down.source_dir={sweep_dir}/",
                f"hydra.launcher.sync_down.target_dir={sweep_dir}",
                f"hydra.launcher.ray_cluster_cfg.provider.key_pair.key_name=hydra_test_{cluster_name}",
                "hydra.launcher.ray_cluster_cfg.setup_commands=[]",
                f"+hydra.launcher.ray_cluster_cfg.worker_nodes={ray_nodes_conf_override}",
                f"+hydra.launcher.ray_cluster_cfg.head_node={ray_nodes_conf_override}",
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
                f"hydra.launcher.ray_cluster_cfg.cluster_name={cluster_name}",
                "hydra.launcher.stop_cluster=False",
                f"hydra.launcher.sync_down.source_dir={temp_remote_dir}/",
                f"hydra.launcher.sync_down.target_dir={temp_remote_dir}",
                f"hydra.launcher.ray_cluster_cfg.provider.key_pair.key_name=hydra_test_{cluster_name}",
                "hydra.launcher.ray_cluster_cfg.setup_commands=[]",
                f"+hydra.launcher.ray_cluster_cfg.worker_nodes={ray_nodes_conf_override}",
                f"+hydra.launcher.ray_cluster_cfg.head_node={ray_nodes_conf_override}",
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
