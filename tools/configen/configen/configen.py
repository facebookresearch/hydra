# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import inspect
import logging
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Type

from jinja2 import Environment, PackageLoader, Template
from omegaconf import OmegaConf, ValidationError
from omegaconf._utils import (
    _is_union,
    _resolve_optional,
    get_dict_key_value_types,
    get_list_element_type,
    is_dict_annotation,
    is_list_annotation,
    is_primitive_type,
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
    if type_ is type(None):  # noqa
        return False
    try:
        if is_list_annotation(type_):
            lt = get_list_element_type(type_)
            return _is_passthrough(lt)
        if is_dict_annotation(type_):
            kvt = get_dict_key_value_types(type_)
            if not issubclass(kvt[0], (str, Enum)):
                return True
            return _is_passthrough(kvt[1])
    except ValidationError:
        return True

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


def collect_imports(imports: Set[Type], type_: Type) -> None:
    if is_list_annotation(type_):
        collect_imports(imports, get_list_element_type(type_))
        type_ = List
    elif is_dict_annotation(type_):
        kvt = get_dict_key_value_types(type_)
        collect_imports(imports, kvt[0])
        collect_imports(imports, kvt[1])
        type_ = Dict
    else:
        is_optional = _resolve_optional(type_)[0]
        if is_optional and type_ is not Any:
            type_ = Optional
    imports.add(type_)


def convert_imports(imports: Set[Type]) -> List[str]:
    res = []
    for t in imports:
        s = None
        if t is Any:
            classname = "Any"
        elif t is Optional:
            classname = "Optional"
        elif t is List:
            classname = "List"
        elif t is Dict:
            classname = "Dict"
        else:
            classname = t.__name__

        if not is_primitive_type(t) or issubclass(t, Enum):
            s = f"from {t.__module__} import {classname}"

        if s is not None:
            res.append(s)
    return sorted(res)


def generate_module(cfg: ConfigenConf, module: ModuleConf) -> str:
    classes_map: Dict[str, ClassInfo] = {}
    imports = set()
    for class_name in module.classes:
        full_name = f"{module.name}.{class_name}"
        cls = hydra.utils.get_class(full_name)
        sig = inspect.signature(cls)
        params: List[Parameter] = []
        for name, p in sig.parameters.items():
            type_ = p.annotation
            default_ = p.default

            is_optional = False
            if type_ == sig.empty:
                type_ = Any
            else:
                resolved_optional = _resolve_optional(type_)
                is_optional = resolved_optional[0]

            # Unions are not supported (Except Optional)
            if not is_optional and _is_union(type_):
                type_ = Any

            passthrough_value = False
            if default_ != sig.empty:
                if type_ == str:
                    default_ = f'"{default_}"'
                elif is_list_annotation(type_):
                    default_ = f"field(default_factory={p.default})"
                elif is_dict_annotation(type_):
                    default_ = f"field(default_factory={p.default})"

                passthrough_value = _is_passthrough(type(default_))

            # fields that are incompatible with the config are flagged as passthrough and are added as a comment
            passthrough = _is_passthrough(type_) or passthrough_value

            if not passthrough:
                collect_imports(imports, type_)

            params.append(
                Parameter(
                    name=name,
                    type_str=type_str(type_),
                    default=default_,
                    passthrough=passthrough,
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
        imports=convert_imports(imports),
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
