# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os

import boto3
from omegaconf import DictConfig

import hydra
from hydra.utils import get_original_cwd

log = logging.getLogger(__name__)


@hydra.main(config_path="config")
def upload_to_s3(cfg: DictConfig) -> None:
    if not os.path.isabs(cfg.local_file_path):
        file_path = os.path.join(get_original_cwd(), cfg.local_file_path)
    else:
        file_path = cfg.local_file_path

    _, file_name = os.path.split(file_path)

    if not file_name:
        log.error("Please pass in a path to a file.")
        return

    client = boto3.Session(profile_name=cfg.aws_config_profile).client("s3")

    client.upload_file(
        file_path, cfg.bucket_name, cfg.s3_file_name if cfg.s3_file_name else file_name
    )

    log.info("Uploaded successfully.")


if __name__ == "__main__":
    upload_to_s3()
