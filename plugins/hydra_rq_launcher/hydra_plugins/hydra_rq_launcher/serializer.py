# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import cloudpickle  # type: ignore


class CloudpickleSerializer:
    dumps = cloudpickle.dumps
    loads = cloudpickle.loads
