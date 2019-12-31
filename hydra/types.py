# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import Any, Callable

import omegaconf

TaskFunction = Callable[[omegaconf.DictConfig], Any]
