import copy
from dataclasses import dataclass
from textwrap import dedent
from typing import Dict, List, Optional, Union

from hydra import MissingConfigException
from hydra._internal.config_repository import IConfigRepository
from hydra.core.NewDefaultElement import ConfigDefault, GroupDefault, InputDefault
from hydra.core.object_type import ObjectType
from hydra.core.override_parser.types import Override


@dataclass
class DefaultsTreeNode:
    parent: InputDefault
    children: Optional[List[Union["DefaultsTreeNode", InputDefault]]] = None


@dataclass
class ResultDefault:
    config_path: Optional[str] = None
    parent: Optional[str] = None
    addressing_key: Optional[str] = None
    result_package: Optional[str] = None
    is_self: bool = False


@dataclass
class Overrides:
    override_choices: Dict[str, str]
    append_group_defaults: List[GroupDefault]
    config_overrides: List[Override]

    def __init__(self, repo: IConfigRepository, overrides_list: List[Override]) -> None:
        self.override_choices = {}
        self.append_group_defaults = []
        self.config_overrides = []

        for override in overrides_list:
            is_group = repo.group_exists(override.key_or_group)
            value = override.value()
            if not is_group:
                self.config_overrides.append(override)
            else:
                if not isinstance(value, str):
                    raise ValueError(
                        f"Config group override must be a string : {override}"
                    )
                if override.is_add():
                    self.append_group_defaults.append(
                        GroupDefault(group=override.key_or_group, name=value)
                    )
                else:
                    self.override_choices[override.key_or_group] = value

    def is_overridden(self, default: InputDefault) -> bool:
        if isinstance(default, GroupDefault):
            key = default.group  # TODO: use package if present
            return key in self.override_choices

        return False

    def get_choice_for(self, default: InputDefault) -> str:
        if isinstance(default, GroupDefault):
            key = default.group  # TODO: use package if present
            if key in self.override_choices:
                return self.override_choices[key]
            else:
                return default.name
        else:
            assert isinstance(default, ConfigDefault)
            return default.path


@dataclass
class DefaultsList:
    defaults: List[ResultDefault]
    config_overrides: List[Override]


def load_config_defaults_list(
    default: InputDefault, group_overrides: Dict[str, str]
) -> List[InputDefault]:
    ...


def _create_defaults_tree(
    repo: IConfigRepository,
    root: DefaultsTreeNode,
    is_primary_config: bool,
    overrides: Overrides,
) -> DefaultsTreeNode:
    assert root.children is None

    if is_primary_config:
        root.parent.parent_base_dir = ""

    parent = root.parent
    if isinstance(parent, GroupDefault):
        if overrides.is_overridden(parent):
            override_name = overrides.get_choice_for(parent)
            parent.name = override_name
            parent.config_name_overridden = True
        path = parent.get_config_path()
    else:
        assert isinstance(parent, ConfigDefault)
        path = parent.path

    loaded = repo.load_config(config_path=path, is_primary_config=is_primary_config)

    if loaded is None:
        missing_config_error(repo, root.parent)
    else:

        defaults_list = copy.deepcopy(loaded.new_defaults_list)
        if is_primary_config:
            for d in overrides.append_group_defaults:
                defaults_list.append(d)

        children = []
        for d in defaults_list:
            if d.is_self():
                d.parent_base_dir = root.parent.parent_base_dir
                children.append(d)
            else:
                new_root = DefaultsTreeNode(parent=d)
                d.parent_base_dir = parent.get_group_path()
                new_root.parent_base_dir = d.get_group_path()
                subtree = _create_defaults_tree(
                    repo=repo,
                    root=new_root,
                    is_primary_config=False,
                    overrides=overrides,
                )
                if subtree.children is None:
                    children.append(d)
                else:
                    children.append(subtree)

        if len(children) > 0:
            root.children = children
    return root


def _create_defaults_list(
    repo: IConfigRepository,
    config_name: str,
    overrides: Overrides,
) -> List[ResultDefault]:
    primary = ConfigDefault(path=config_name)
    root = DefaultsTreeNode(parent=primary)
    defaults_tree = _create_defaults_tree(
        repo=repo,
        root=root,
        overrides=overrides,
        is_primary_config=True,
    )
    # TODO: convert tree to list with DFS
    # TODO: fail if duplicate items exists
    return []


def create_defaults_list(
    repo: IConfigRepository,
    config_name: str,
    overrides_list: List[Override],
) -> DefaultsList:
    overrides = Overrides(repo=repo, overrides_list=overrides_list)
    defaults = _create_defaults_list(repo, config_name, overrides)
    ret = DefaultsList(defaults=defaults, config_overrides=overrides.config_overrides)
    return ret


def missing_config_error(repo: IConfigRepository, element: InputDefault) -> None:
    options = None
    if isinstance(element, GroupDefault) is not None:
        options = repo.get_group_options(element.group, ObjectType.CONFIG)
        opt_list = "\n".join(["\t" + x for x in options])
        msg = (
            f"Could not find '{element.name}' in the config group '{element.get_group_path()}'"
            f"\nAvailable options:\n{opt_list}\n"
        )
    else:
        msg = dedent(
            f"""\
        Could not load {element.get_config_path()}.
        """
        )

    descs = []
    for src in repo.get_sources():
        descs.append(f"\t{repr(src)}")
    lines = "\n".join(descs)
    msg += "\nConfig search path:" + f"\n{lines}"

    raise MissingConfigException(
        missing_cfg_file=element.get_config_path(),
        message=msg,
        options=options,
    )
