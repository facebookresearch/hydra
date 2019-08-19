# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import inspect
import os
from os.path import realpath, dirname

from .hydra import Hydra


def run_hydra(args, task_function, config_path, strict):
    stack = inspect.stack()
    calling_file = stack[2][0].f_locals["__file__"]

    target_file = os.path.basename(calling_file)
    task_name = os.path.splitext(target_file)[0]

    abs_base_dir = realpath(dirname(calling_file))
    hydra = Hydra(
        abs_base_dir=abs_base_dir,
        task_name=task_name,
        config_path=config_path,
        task_function=task_function,
        verbose=args.verbose,
        strict=strict,
    )

    if args.run + args.cfg + args.multirun > 1:
        raise ValueError("Only one of --run, --sweep and --cfg can be specified")
    if args.run + args.cfg + args.multirun == 0:
        args.run = True

    if args.run:
        command = "run"
    elif args.sweep:
        raise RuntimeError("-s|--sweep is no longer supported, please us -m|--multirun")
    elif args.multirun:
        command = "multirun"
    elif args.cfg:
        command = "cfg"

    if command == "run":
        hydra.run(overrides=args.overrides)
    elif command == "multirun":
        hydra.multirun(overrides=args.overrides)
    elif command == "cfg":
        hydra.show_cfg(overrides=args.overrides)
    else:
        print("Command not specified")
