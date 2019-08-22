# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
class MissingConfigException(IOError):
    def __init__(self, message, missing_cfg_file, options=[]):
        super(MissingConfigException, self).__init__(message)
        self.missing_cfg_file = missing_cfg_file
        self.options = options
