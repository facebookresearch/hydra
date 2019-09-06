# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import inspect
import os
import sys
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
        module_envs = ["HYDRA_MAIN_MODULE", "FB_PAR_MAIN_MODULE", "FB_XAR_MAIN_MODULE"]
        for module_env in module_envs:
            if module_env in os.environ:
                calling__module = os.environ[module_env]
                break

        if calling__module is None:
            calling__module = frame[0].f_globals[frame[3]].__module__
    except KeyError:
        pass

    hydra = Hydra(
        calling_file=calling_file,
        calling_module=calling__module,
        config_path=config_path,
        task_function=task_function,
        verbose=args.verbose,
        strict=strict,
    )

    num_commands = args.run + args.cfg + args.multirun + args.shell_completion
    if num_commands > 1:
        raise ValueError(
            "Only one of --run, --sweep and --cfg  --completion can be specified"
        )
    if num_commands == 0:
        args.run = True

    if args.run:
        hydra.run(overrides=args.overrides)
    elif args.multirun:
        hydra.multirun(overrides=args.overrides)
    elif args.cfg:
        hydra.show_cfg(overrides=args.overrides)
    elif args.shell_completion:
        hydra.shell_completion(overrides=args.overrides)
    else:
        print("Command not specified")
        sys.exit(1)
