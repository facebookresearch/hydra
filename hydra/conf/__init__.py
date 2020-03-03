# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from omegaconf import MISSING

from hydra.core.config_store import ConfigStore

hydra_defaults = [
    # Hydra's logging config
    {"hydra/hydra_logging": "default"},
    # Job's logging config
    {"hydra/job_logging": "default"},
    # Launcher config
    {"hydra/launcher": "basic"},
    # Sweeper config
    {"hydra/sweeper": "basic"},
    # Output directory
    {"hydra/output": "default"},
    # --help template
    {"hydra/help": "default"},
    # --hydra-help template
    {"hydra/hydra_help": "default"},
]


@dataclass
# This extends Dict[str, Any] to allow for the deprecated "class" field.
# Once support for class field removed this can stop extending Dict.
class PluginConf(Dict[str, Any]):
    # class name for plugin
    cls: str = MISSING
    params: Any = field(default_factory=dict)


@dataclass
class HelpConf:
    app_name: str = MISSING
    header: str = MISSING
    footer: str = MISSING
    template: str = MISSING


@dataclass
class HydraHelpConf:
    hydra_help: str = MISSING
    template: str = MISSING


@dataclass
class RunDir:
    dir: str = MISSING


@dataclass
class SweepDir:
    dir: str = MISSING
    subdir: str = MISSING


@dataclass
class OverridesConf:
    # Overrides for the hydra configuration
    hydra: List[str] = field(default_factory=lambda: [])
    # Overrides for the task configuration
    task: List[str] = field(default_factory=lambda: [])


@dataclass
# job runtime information will be populated here
class JobConf:
    # Job name, can be specified by the user (in config or cli) or populated automatically
    name: str = MISSING

    # Concatenation of job overrides that can be used as a part
    # of the directory name.
    # This can be configured in hydra.job.config.override_dirname
    override_dirname: str = MISSING

    # Job ID in underlying scheduling system
    id: str = MISSING

    # Job number if job is a part of a sweep
    num: str = MISSING

    # The config name used by the job
    config_name: Optional[str] = MISSING

    @dataclass
    # Job config
    class JobConfig:
        @dataclass
        # configuration for the ${hydra.job.override_dirname} runtime variable
        class OverrideDirname:
            kv_sep: str = "="
            item_sep: str = ","
            exclude_keys: List[str] = field(default_factory=lambda: [])

        override_dirname: OverrideDirname = OverrideDirname()

    config: JobConfig = JobConfig()


@dataclass
class RuntimeConf:
    version: str = MISSING
    cwd: str = MISSING


@dataclass
class HydraConf:
    # Normal run output configuration
    run: RunDir = RunDir()
    # Multi-run output configuration
    sweep: SweepDir = SweepDir()
    # Logging configuration for Hydra
    hydra_logging: Any = MISSING
    # Logging configuration for the job
    job_logging: Any = MISSING

    # Sweeper configuration
    sweeper: PluginConf = field(default_factory=PluginConf)
    # Launcher configuration
    launcher: PluginConf = field(default_factory=PluginConf)

    # Program Help template
    help: HelpConf = HelpConf()
    # Hydra's Help template
    hydra_help: HydraHelpConf = HydraHelpConf()

    # Output directory for produced configuration files and overrides.
    # E.g., hydra.yaml, overrides.yaml will go here. Useful for debugging
    # and extra context when looking at past runs.
    output_subdir: str = ".hydra"

    # Those lists will contain runtime overrides
    overrides: OverridesConf = OverridesConf()

    job: JobConf = JobConf()

    # populated at runtime
    runtime: RuntimeConf = RuntimeConf()

    # Can be a boolean, string or a list of strings
    # If a boolean, setting to true will set the log level for the root logger to debug
    # If a string, it's interpreted as a the list [string]
    # If a list, each element is interpreted as a logger to have logging level set to debug.
    # Typical command lines to manipulate hydra.verbose:
    # hydra.verbose=true
    # hydra.verbose=[hydra,__main__]
    # TODO: good use case for Union support in OmegaConf
    verbose: Any = False


ConfigStore.instance().store(
    name="hydra_config",
    node={
        # Hydra composition defaults
        "defaults": hydra_defaults,
        # Hydra config
        "hydra": HydraConf,
    },
    provider="hydra",
)
