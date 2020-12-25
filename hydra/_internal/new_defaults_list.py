from dataclasses import dataclass
from textwrap import dedent
from typing import Dict, List, Optional, Tuple, Union

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
class GroupOverrides:
    map: Dict[str, str]

    def is_overridden(self, default: InputDefault) -> bool:
        if isinstance(default, GroupDefault):
            key = default.group  # TODO: use package if present
            return key in self.map

        return False

    def get_choice_for(self, default: InputDefault) -> str:
        if isinstance(default, GroupDefault):
            key = default.group  # TODO: use package if present
            if key in self.map:
                return self.map[key]
            else:
                return default.name
        else:
            assert isinstance(default, ConfigDefault)
            return default.path


@dataclass
class DefaultsList:
    defaults: List[ResultDefault]
    config_overrides: List[Override]


def _split_overrides(
    repo: IConfigRepository,
    overrides: List[Override],
) -> Tuple[List[Override], List[Override]]:
    # TODO
    return overrides, []


def _create_group_overrides(default_overrides: List[Override]) -> GroupOverrides:
    group_overrides = GroupOverrides(map={})
    for override in default_overrides:
        value = override.value()
        assert isinstance(value, str)
        group_overrides.map[override.key_or_group] = value

    return group_overrides


def load_config_defaults_list(
    default: InputDefault, group_overrides: Dict[str, str]
) -> List[InputDefault]:
    ...


def _create_defaults_tree(
    repo: IConfigRepository,
    root: DefaultsTreeNode,
    is_primary_config: bool,
    group_overrides: GroupOverrides,
) -> DefaultsTreeNode:
    assert root.children is None

    parent = root.parent
    if isinstance(parent, GroupDefault):
        if group_overrides.is_overridden(parent):
            override_name = group_overrides.get_choice_for(parent)
            parent.name = override_name
            parent.config_name_overridden = True
        path = parent.get_config_path()
    else:
        assert isinstance(parent, ConfigDefault)
        path = parent.path

    if is_primary_config:
        root.parent.parent_base_dir = ""

    loaded = repo.load_config(config_path=path, is_primary_config=is_primary_config)

    if loaded is None:
        missing_config_error(repo, root.parent)
    else:
        children = []
        for d in loaded.new_defaults_list:
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
                    group_overrides=group_overrides,
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
    default_overrides: List[Override],
) -> List[ResultDefault]:
    group_overrides = _create_group_overrides(default_overrides)
    primary = ConfigDefault(path=config_name)
    root = DefaultsTreeNode(parent=primary)
    defaults_tree = _create_defaults_tree(
        repo=repo,
        root=root,
        group_overrides=group_overrides,
        is_primary_config=True,
    )
    # TODO: convert tree to list with DFS
    # TODO: fail if duplicate items exists
    return []


def create_defaults_list(
    repo: IConfigRepository,
    config_name: str,
    overrides: List[Override],
) -> DefaultsList:
    default_overrides, config_overrides = _split_overrides(repo, overrides)
    defaults = _create_defaults_list(repo, config_name, default_overrides)
    ret = DefaultsList(defaults=defaults, config_overrides=config_overrides)
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
