# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
def foo() -> None: ...


def foo_main_module() -> None: ...


foo_main_module.__module__ = "__main__"


class Bar: ...


bar_instance = Bar()

bar_instance_main_module = Bar()
bar_instance_main_module.__module__ = "__main__"
