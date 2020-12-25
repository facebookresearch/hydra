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
    override_used: Dict[str, bool]

    append_group_defaults: List[GroupDefault]
    config_overrides: List[Override]

    def __init__(self, repo: IConfigRepository, overrides_list: List[Override]) -> None:
        self.override_choices = {}
        self.override_used = {}
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
                        GroupDefault(
                            group=override.key_or_group,
                            package=override.get_subject_package(),
                            name=value,
                        )
                    )
                else:
                    key = override.get_key_element()
                    self.override_choices[key] = value
                    self.override_used[key] = False

    def is_overridden(self, default: InputDefault) -> bool:
        if isinstance(default, GroupDefault):
            return default.get_override_key() in self.override_choices

        return False

    def override_default_option(self, default: GroupDefault) -> None:
        key = default.get_override_key()
        if key in self.override_choices:
            default.name = self.override_choices[key]
            default.config_name_overridden = True
            self.override_used[key] = True

    def ensure_overrides_used(self):
        for key, used in self.override_used.items():
            if not used:
                msg = dedent(
                    f"""\
                    Could not override '{key}'. No match in the defaults list.
                    To append to your default list use +{key}={self.override_choices[key]}"""
                )
                raise ConfigCompositionException(msg)


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
        root.node.parent_package = ""

    parent = root.node
    if isinstance(parent, GroupDefault):
        if overrides.is_overridden(parent):
            overrides.override_default_option(parent)

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
                d.parent_package = root.node.parent_package
                children.append(d)
            else:
                new_root = DefaultsTreeNode(node=d, parent=root)
                d.parent_base_dir = parent.get_group_path()
                d.parent_package = parent.get_final_package()
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
        if pn is not None:
            cp = pn.get_config_path()
            res.parent = cp
        else:
            res.parent = None
        res.package = tree.node.get_final_package()
    else:
        res.config_path = node.get_config_path()
        if tree is not None:
            res.parent = tree.node.get_config_path()
        res.package = node.get_final_package()
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
    # TODO: fail if duplicate items exists
    return output


def create_defaults_list(
    repo: IConfigRepository,
    config_name: str,
    overrides_list: List[Override],
) -> DefaultsList:
    overrides = Overrides(repo=repo, overrides_list=overrides_list)
    defaults = _create_defaults_list(repo, config_name, overrides)
    overrides.ensure_overrides_used()
    ret = DefaultsList(defaults=defaults, config_overrides=overrides.config_overrides)
    return ret


# TODO: show parent config name in the error (where is my error?)
def missing_config_error(repo: IConfigRepository, element: InputDefault) -> None:
    options = None
    if isinstance(element, GroupDefault):
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
