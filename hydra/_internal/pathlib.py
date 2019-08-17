# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import six

if six.PY2:
    from pathlib2 import Path
else:
    from pathlib import Path

__all__ = ["Path"]
