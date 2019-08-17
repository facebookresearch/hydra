# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import inspect
import os


def run_hydra(args, task_function, config_path, strict):
    stack = inspect.stack()
    calling_file = stack[2][0].f_locals["__file__"]

    target_file = os.path.basename(calling_file)
    task_name = os.path.splitext(target_file)[0]

    if os.path.isabs(config_path):
        raise RuntimeError("Config path should be relative")
    abs_config_path = os.path.realpath(
        os.path.join(os.path.dirname(calling_file), config_path)
    )
    if not os.path.exists(abs_config_path):
        raise RuntimeError("Config path '{}' does not exist".format(abs_config_path))
    if os.path.isfile(abs_config_path):
        conf_dir = os.path.dirname(abs_config_path)
        conf_filename = os.path.basename(abs_config_path)
    else:
        conf_dir = abs_config_path
        conf_filename = None

    from .hydra import Hydra

    hydra = Hydra(
        task_name=task_name,
        conf_dir=conf_dir,
        conf_filename=conf_filename,
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
