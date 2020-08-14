# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import inspect
import logging
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, List, Optional, Type

from jinja2 import Environment, PackageLoader, Template
from omegaconf import OmegaConf, ValidationError
from omegaconf._utils import _is_union, is_structured_config, type_str

import hydra
from configen.config import Config, ConfigenConf

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


def save(cfg: ConfigenConf, module: str, classname: str, code: str) -> None:
    module_path = module.replace(".", "/")

    module_dir = Template(cfg.module_dir).render(module_path=module_path)
    path = Path(cfg.output_dir) / module_dir
    path.mkdir(parents=True, exist_ok=True)
    file = path / (classname + ".py")
    file.unlink(missing_ok=True)
    file.write_text(code)
    log.info(f"{module}.{classname} -> {file}")


@dataclass
class Parameter:
    name: str
    type_str: str
    default: Optional[str]
    passthrough: bool


def _is_passthrough(type_: Type[Any]) -> bool:
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


def generate(cfg: ConfigenConf, module_name: str, class_name: str) -> str:
    full_name = f"{module_name}.{class_name}"
    cls = hydra.utils.get_class(full_name)
    sig = inspect.signature(cls)
    template = jinja_env.get_template("dataclass.j2")
    params: List[Parameter] = []
    for name, p in sig.parameters.items():
        type_ = p.annotation
        if type_ == sig.empty or _is_union(type_):
            type_ = Any
        params.append(
            Parameter(
                name=name,
                type_str=type_str(type_),
                default=p.default,
                passthrough=_is_passthrough(type_),
            )
        )
    return template.render(
        target=f'"{full_name}"', class_name=class_name, params=params, header=cfg.header
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
        for class_name in module.classes:
            code = generate(
                cfg=cfg.configen, module_name=module.name, class_name=class_name
            )
            save(cfg=cfg.configen, module=module.name, classname=class_name, code=code)


if __name__ == "__main__":
    main()
