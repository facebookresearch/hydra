import copy
from dataclasses import dataclass
from textwrap import dedent
from typing import Dict, List

from hydra import MissingConfigException
from hydra._internal.config_repository import IConfigRepository
from hydra.core.new_default_element import (
    ConfigDefault,
    DefaultsTreeNode,
    GroupDefault,
    InputDefault,
    ResultDefault,
)
from hydra.core.object_type import ObjectType
from hydra.core.override_parser.types import Override
from hydra.errors import ConfigCompositionException


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
            key = default.get_group_path()  # TODO: use package if present
            return key in self.override_choices

        return False

    def get_choice_for(self, default: InputDefault) -> str:
        if isinstance(default, GroupDefault):
            key = default.get_group_path()  # TODO: use package if present
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


def _validate_self(containing_node: InputDefault, defaults: List[InputDefault]) -> None:
    # check that self is present only once
    has_self = False
    for d in defaults:
        if d.is_self():
            if has_self:
                raise ConfigCompositionException(
                    f"Duplicate _self_ defined in {containing_node.get_config_path()}"
                )
            has_self = True

    if not has_self:
        defaults.insert(0, ConfigDefault(path="_self_"))


def _create_defaults_tree(
    repo: IConfigRepository,
    root: DefaultsTreeNode,
    is_primary_config: bool,
    overrides: Overrides,
) -> DefaultsTreeNode:
    assert root.children is None

    if is_primary_config:
        root.node.parent_base_dir = ""

    parent = root.node
    if isinstance(parent, GroupDefault):
        if overrides.is_overridden(parent):
            override_name = overrides.get_choice_for(parent)
            parent.name = override_name
            parent.config_name_overridden = True

    path = parent.get_config_path()

    loaded = repo.load_config(config_path=path, is_primary_config=is_primary_config)

    if loaded is None:
        missing_config_error(repo, root.node)
    else:
        defaults_list = copy.deepcopy(loaded.new_defaults_list)
        if is_primary_config:
            for d in overrides.append_group_defaults:
                defaults_list.append(d)

        if len(defaults_list) > 0:
            _validate_self(containing_node=parent, defaults=defaults_list)

        children = []
        for d in defaults_list:
            if d.is_self():
                d.parent_base_dir = root.node.parent_base_dir
                children.append(d)
            else:
                new_root = DefaultsTreeNode(node=d, parent=root)
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


def _create_result_default(tree: DefaultsTreeNode, node: InputDefault) -> ResultDefault:
    res = ResultDefault()
    if node.is_self():
        res.config_path = tree.node.get_config_path()
        res.is_self = True
        pn = tree.parent_node()
        cp = pn.get_config_path() if pn is not None else None
        res.parent = cp
    else:
        res.config_path = node.get_config_path()
        if tree is not None:
            res.parent = tree.node.get_config_path()
    return res


def _tree_to_list(
    tree: DefaultsTreeNode,
    output: List[ResultDefault],
):
    node = tree.node

    if tree.children is None or len(tree.children) == 0:
        rd = _create_result_default(tree=tree.parent, node=node)
        output.append(rd)
    else:
        for child in tree.children:
            if isinstance(child, InputDefault):
                rd = _create_result_default(tree=tree, node=child)
                output.append(rd)
            else:
                assert isinstance(child, DefaultsTreeNode)
                _tree_to_list(tree=child, output=output)


def _create_defaults_list(
    repo: IConfigRepository,
    config_name: str,
    overrides: Overrides,
) -> List[ResultDefault]:
    primary = ConfigDefault(path=config_name)
    root = DefaultsTreeNode(node=primary)
    defaults_tree = _create_defaults_tree(
        repo=repo,
        root=root,
        overrides=overrides,
        is_primary_config=True,
    )

    output = []
    _tree_to_list(tree=defaults_tree, output=output)
    # TODO: convert tree to list with DFS
    # TODO: fail if duplicate items exists
    return output


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
