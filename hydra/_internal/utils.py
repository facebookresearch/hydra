# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import inspect
import os
from os.path import realpath, dirname

from .hydra import Hydra


def run_hydra(args, task_function, config_path, strict):
    stack = inspect.stack()
    frame = stack[2]

    calling_file = None
    calling__module = None
    try:
        calling_file = frame[0].f_locals["__file__"]
    except KeyError:
        pass
    try:
        calling__module = frame[0].f_globals[frame[3]].__module__
    except KeyError:
        pass

    # print("calling module", calling__module)
    # print("calling file", calling_file)

    if calling__module is None:
        # executed with python file.py
        abs_base_dir = realpath(dirname(calling_file))
        target_file = os.path.basename(calling_file)
        task_name = os.path.splitext(target_file)[0]
    else:
        # module is installed, use pkg:// access to get configs
        abs_base_dir = "pkg://" + calling__module
        task_name = "TODO"
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
