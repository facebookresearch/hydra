# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import copy
import logging
import pickle
from pathlib import Path
from typing import Any, List, Optional

from omegaconf import DictConfig, flag_override, OmegaConf

from hydra.core.global_hydra import GlobalHydra
from hydra.core.utils import JobReturn, JobStatus
from hydra.experimental.callback import Callback
from hydra.types import RunMode


class LogJobReturnCallback(Callback):
    """Log the job's return value or error upon job end"""

    def __init__(self) -> None:
        self.log = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def on_job_end(
        self, config: DictConfig, job_return: JobReturn, **kwargs: Any
    ) -> None:
        if job_return.status == JobStatus.COMPLETED:
            self.log.info(f"Succeeded with return value: {job_return.return_value}")
        elif job_return.status == JobStatus.FAILED:
            self.log.error("", exc_info=job_return._return_value)
        else:
            self.log.error("Status unknown. This should never happen.")


class PickleJobInfoCallback(Callback):
    """Pickle the job config/return-value in ${output_dir}/{config,job_return}.pickle"""

    output_dir: Path

    def __init__(self) -> None:
        self.log = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def on_job_start(self, config: DictConfig, **kwargs: Any) -> None:
        """Pickle the job's config in ${output_dir}/config.pickle."""
        self.output_dir = Path(config.hydra.runtime.output_dir) / Path(
            config.hydra.output_subdir
        )
        filename = "config.pickle"
        self._save_pickle(obj=config, filename=filename, output_dir=self.output_dir)
        self.log.info(f"Saving job configs in {self.output_dir / filename}")

    def on_job_end(
        self, config: DictConfig, job_return: JobReturn, **kwargs: Any
    ) -> None:
        """Pickle the job's return value in ${output_dir}/job_return.pickle."""
        filename = "job_return.pickle"
        self._save_pickle(obj=job_return, filename=filename, output_dir=self.output_dir)
        self.log.info(f"Saving job_return in {self.output_dir / filename}")

    def _save_pickle(self, obj: Any, filename: str, output_dir: Path) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)
        assert output_dir is not None
        with open(str(output_dir / filename), "wb") as file:
            pickle.dump(obj, file, protocol=4)


class LogComposeCallback(Callback):
    """Log compose call, result, and debug info"""

    def __init__(self) -> None:
        self.log = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def on_compose_config(
        self,
        config: DictConfig,
        config_name: Optional[str],
        overrides: List[str],
    ) -> None:
        gh = GlobalHydra.instance()
        config_loader = gh.config_loader()
        config_dir = "unknown"
        defaults_list = config_loader.compute_defaults_list(
            config_name, overrides, RunMode.RUN
        )
        all_sources = config_loader.get_sources()
        if config_name:
            for src in all_sources:
                if src.is_config(config_name):
                    config_dir = src.full_path()
                    break
        if "hydra" in config:
            config = copy.copy(config)
            with flag_override(config, ["struct", "readonly"], [False, False]):
                config.pop("hydra")
        non_hydra_defaults = [
            d.config_path
            for d in defaults_list.defaults
            if not d.package.startswith("hydra")
        ]
        self.log.info(
            f"""
====
Composed config {config_dir}/{str(config_name)}
{OmegaConf.to_yaml(config)}
----
Includes overrides {overrides}
Used defaults {non_hydra_defaults}
===="""
        )
