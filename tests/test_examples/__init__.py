# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from subprocess import PIPE, Popen
from typing import Any


def run_with_error(cmd: Any, env: Any = None) -> str:
    with Popen(cmd, stdout=PIPE, stderr=PIPE, env=env) as p:
        _stdout, stderr = p.communicate()
        err = stderr.decode("utf-8").rstrip().replace("\r\n", "\n")
        assert p.returncode == 1
    return err
