# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from omegaconf import MISSING

from hydra.core.config_store import ConfigStore
from hydra.types import RunMode


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


# job runtime information will be populated here
@dataclass
class JobConf:
    # Job name, populated automatically unless specified by the user (in config or cli)
    name: str = MISSING

    # Change current working dir to the output dir.
    # Will be non-optional and default to False in Hydra 1.3
    chdir: Optional[bool] = None

    # Populated automatically by Hydra.
    # Concatenation of job overrides that can be used as a part
    # of the directory name.
    # This can be configured via hydra.job.config.override_dirname
    override_dirname: str = MISSING

    # Job ID in underlying scheduling system
    id: str = MISSING

    # Job number if job is a part of a sweep
    num: int = MISSING

    # The config name used by the job
    config_name: Optional[str] = MISSING

    # Environment variables to set remotely
    env_set: Dict[str, str] = field(default_factory=dict)
    # Environment variables to copy from the launching machine
    env_copy: List[str] = field(default_factory=list)

    # Job config
    @dataclass
    class JobConfig:
        @dataclass
        # configuration for the ${hydra.job.override_dirname} runtime variable
        class OverrideDirname:
            kv_sep: str = "="
            item_sep: str = ","
            exclude_keys: List[str] = field(default_factory=list)

        override_dirname: OverrideDirname = field(default_factory=OverrideDirname)

    config: JobConfig = field(default_factory=JobConfig)


@dataclass
class ConfigSourceInfo:
    path: str
    schema: str
    provider: str


@dataclass
class RuntimeConf:
    version: str = MISSING
    version_base: str = MISSING
    cwd: str = MISSING
    config_sources: List[ConfigSourceInfo] = MISSING
    output_dir: str = MISSING

    # Composition choices dictionary
    # Ideally, the value type would be Union[str, List[str], None]
    choices: Dict[str, Any] = field(default_factory=lambda: {})


@dataclass
class HydraConf:
    defaults: List[Any] = field(
        default_factory=lambda: [
            {"output": "default"},
            {"launcher": "basic"},
            {"sweeper": "basic"},
            {"help": "default"},
            {"hydra_help": "default"},
            {"hydra_logging": "default"},
            {"job_logging": "default"},
            {"callbacks": None},
            # env specific overrides
            {"env": "default"},
        ]
    )

    mode: Optional[RunMode] = None
    # Elements to append to the config search path.
    # Note: This can only be configured in the primary config.
    searchpath: List[str] = field(default_factory=list)

    # Normal run output configuration
    run: RunDir = field(default_factory=RunDir)
    # Multi-run output configuration
    sweep: SweepDir = field(default_factory=SweepDir)
    # Logging configuration for Hydra
    hydra_logging: Dict[str, Any] = MISSING
    # Logging configuration for the job
    job_logging: Dict[str, Any] = MISSING

    # Sweeper configuration
    sweeper: Any = MISSING
    # Launcher configuration
    launcher: Any = MISSING
    # Callbacks configuration
    callbacks: Dict[str, Any] = field(default_factory=dict)

    # Program Help template
    help: HelpConf = field(default_factory=HelpConf)
    # Hydra's Help template
    hydra_help: HydraHelpConf = field(default_factory=HydraHelpConf)

    # Output directory for produced configuration files and overrides.
    # E.g., hydra.yaml, overrides.yaml will go here. Useful for debugging
    # and extra context when looking at past runs.
    # Setting to None will prevent the creation of the output subdir.
    output_subdir: Optional[str] = ".hydra"

    # Those lists will contain runtime overrides
    overrides: OverridesConf = field(default_factory=OverridesConf)

    job: JobConf = field(default_factory=JobConf)

    # populated at runtime
    runtime: RuntimeConf = field(default_factory=RuntimeConf)

    # Can be a boolean, string or a list of strings
    # If a boolean, setting to true will set the log level for the root logger to debug
    # If a string, it's interpreted as a the list [string]
    # If a list, each element is interpreted as a logger to have logging level set to debug.
    # Typical command lines to manipulate hydra.verbose:
    # hydra.verbose=true
    # hydra.verbose=[hydra,__main__]
    # TODO: good use case for Union support in OmegaConf
    verbose: Any = False


cs = ConfigStore.instance()

cs.store(
    group="hydra",
    name="config",
    node=HydraConf(),
    provider="hydra",
)
