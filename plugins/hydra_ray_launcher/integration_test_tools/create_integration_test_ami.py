# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

"""
This script is meant to be used for ray launcher integration tests only!

Run this script with AWS admin credentials to create new integration test AMIs if any hydra-core & hydra-ray-launcher
dependencies changes or there's a newer version of python available for testing.

This is needed because our testing EC2 instance doesn't not have outbound internet access and as a result cannot create
conda env on demand.

Please update env variable AWS_RAY_AMI locally and on circleCI with the new AMI id when the new AMI is available.
"""
import os
import subprocess
import tempfile
import time
from datetime import datetime

import boto3
import hydra
from omegaconf import DictConfig, OmegaConf


def _run_command(command: str) -> str:
    print(f"{str(datetime.now())} - Running: {command}")
    output = subprocess.getoutput(command)
    print(f"{str(datetime.now())} - {output}")
    return output


@hydra.main(config_name="create_integration_test_ami_config")
def set_up_machine(cfg: DictConfig) -> None:
    security_group_id = cfg.security_group_id
    assert security_group_id != "", "Security group cannot be empty!"

    # set up security group rules to allow pip install
    _run_command(
        f"aws ec2 authorize-security-group-egress --group-id {security_group_id} "
        f"--ip-permissions IpProtocol=tcp,FromPort=443,ToPort=443,IpRanges=[{{CidrIp=0.0.0.0/0}}]"
    )

    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
        with open(f.name, "w") as file:
            OmegaConf.save(config=cfg.ray_yaml, f=file.name, resolve=True)
        yaml = f.name
        _run_command(f"ray up {yaml} -y")
        os.chdir(hydra.utils.get_original_cwd())
        _run_command(
            f"ray rsync_up {yaml} './setup_integration_test_ami.py' '/home/ubuntu/' "
        )

        print(
            "Installing dependencies now, this may take a while (very likely more than 20 mins) ..."
        )
        _run_command(f"ray exec {yaml} 'python ./setup_integration_test_ami.py' ")

        # remove security group egress rules
        _run_command(
            f"aws ec2 revoke-security-group-egress --group-id {security_group_id} "
            f"--ip-permissions IpProtocol=tcp,FromPort=443,ToPort=443,IpRanges=[{{CidrIp=0.0.0.0/0}}]"
        )

        # export the instance to an AMI
        ec2_resource = boto3.resource("ec2")
        ec2_client = boto3.client("ec2")
        instance_id = None
        for instance in ec2_resource.instances.all():
            for t in instance.tags:
                if (
                    t["Key"] == "Name"
                    and t["Value"] == f"ray-{cfg.ray_yaml.cluster_name}-head"
                    and instance.state["Name"] == "running"
                ):
                    instance_id = instance.id
                    break

        assert instance_id is not None
        try:
            ami_name = f"ray_test_ami_{str(datetime.now()).replace(' ', '_').replace(':', '.')}"

            ret = ec2_client.create_image(InstanceId=instance_id, Name=ami_name)
            image_id = ret.get("ImageId")

            # wait till image is ready, 30 mins for now, this could take a while
            for i in range(60):
                time.sleep(30)
                image = ec2_resource.Image(image_id)
                if image.state == "available":
                    print(
                        f"{image} ready for use now. Please update your env variable: AWS_RAY_AMI={image}. "
                        f"Please also update the test user's IAM policy to allow access to the new AMI."
                    )
                    break
                else:
                    print(f"{image} current state {image.state}")
        finally:
            # Terminate instance now we have the AMI.
            ec2_resource.instances.filter(InstanceIds=[instance_id]).terminate()


if __name__ == "__main__":
    set_up_machine()
