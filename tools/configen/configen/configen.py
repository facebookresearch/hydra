# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import inspect
import logging
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from jinja2 import Environment, PackageLoader, Template
from omegaconf import OmegaConf, ValidationError
from omegaconf._utils import (
    _is_union,
    _resolve_optional,
    is_structured_config,
    type_str,
)

import hydra
from configen.config import Config, ConfigenConf, ModuleConf

log = logging.getLogger(__name__)

jinja_env = Environment(
    loader=PackageLoader("configen", "templates"),
    keep_trailing_newline=True,
    trim_blocks=True,
)
jinja_env.tests["empty"] = lambda x: x == inspect.Signature.empty


def init_config(conf_dir: str) -> None:
    log.info(f"Initializing config in '{conf_dir}'")
    template = jinja_env.get_template("sample_config.yaml")
    path = Path(hydra.utils.to_absolute_path(conf_dir))
    path.mkdir(parents=True, exist_ok=True)
    file = path / "configen.yaml"
    if file.exists():
        raise IOError(f"Config file '{file}' already exists")

    sample_config = template.render()
    file.write_text(sample_config)


def save(cfg: ConfigenConf, module: str, code: str) -> None:
    module_path = module.replace(".", "/")

    module_path_pattern = Template(cfg.module_path_pattern).render(
        module_path=module_path
    )
    path = Path(cfg.output_dir) / module_path_pattern
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(code)
    log.info(f"{module}.{module} -> {path}")


@dataclass
class Parameter:
    name: str
    type_str: str
    default: Optional[str]
    passthrough: bool


@dataclass
class ClassInfo:
    module: str
    name: str
    parameters: List[Parameter]
    target: str


def _is_passthrough(type_: Type[Any]) -> bool:
    type_ = _resolve_optional(type_)[1]
    if type_ is Any or issubclass(type_, (int, float, str, bool, Enum)):
        return False
    if is_structured_config(type_):
        try:
            OmegaConf.structured(type_)  # verify it's actually legal
        except ValidationError as e:
            log.debug(
                f"Failed to create DictConfig from ({type_.__name__}) : {e}, flagging as passthrough"
            )
            return True
        return False
    return True


def generate_module(cfg: ConfigenConf, module: ModuleConf) -> str:
    classes_map: Dict[str, ClassInfo] = {}
    for class_name in module.classes:
        full_name = f"{module.name}.{class_name}"
        cls = hydra.utils.get_class(full_name)
        sig = inspect.signature(cls)
        params: List[Parameter] = []
        for name, p in sig.parameters.items():
            type_ = p.annotation
            default_ = p.default
            if type_ == str and default_ is not inspect._empty:
                default_ = f'"{default_}"'

            optional = _resolve_optional(type_)[0]
            if type_ == sig.empty or (not optional and _is_union(type_)):
                type_ = Any
            params.append(
                Parameter(
                    name=name,
                    type_str=type_str(type_),
                    default=default_,
                    passthrough=_is_passthrough(type_),
                )
            )
        classes_map[class_name] = ClassInfo(
            target=full_name,
            module=module.name,
            name=class_name,
            parameters=params,
        )

    template = jinja_env.get_template("module.j2")
    return template.render(
        classes=module.classes,
        classes_map=classes_map,
        header=cfg.header,
    )


@hydra.main(config_name="configen")
def main(cfg: Config):
    if cfg.init_config_dir is not None:
        init_config(cfg.init_config_dir)
        return

    if OmegaConf.is_missing(cfg.configen, "modules"):  # type: ignore
        log.error(
            "Use --config-dir DIR."
            "\nIf you have no config dir yet use the following command to create an initial config in the `conf` dir:"
            "\n\tconfigen init_config_dir=conf"
        )
        sys.exit(1)

    for module in cfg.configen.modules:
        code = generate_module(cfg=cfg.configen, module=module)
        save(cfg=cfg.configen, module=module.name, code=code)


if __name__ == "__main__":
    main()
