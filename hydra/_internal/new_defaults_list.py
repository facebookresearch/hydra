# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import copy
import warnings
from dataclasses import dataclass
from textwrap import dedent
from typing import Dict, List, Optional, Union

from hydra import MissingConfigException
from hydra._internal.config_repository import IConfigRepository
from hydra.core.new_default_element import (
    ConfigDefault,
    DefaultsTreeNode,
    GroupDefault,
    InputDefault,
    ResultDefault,
    VirtualRoot,
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

    def add_override(self, default: GroupDefault) -> None:
        assert default.override
        key = default.get_override_key()
        if key not in self.override_choices:
            self.override_choices[key] = default.get_name()
            self.override_used[key] = False

    def is_overridden(self, default: InputDefault) -> bool:
        if isinstance(default, GroupDefault):
            # TODO: collect overridable keys for help/useful error purposes
            return default.get_override_key() in self.override_choices

        return False

    def override_default_option(self, default: GroupDefault) -> None:
        key = default.get_override_key()
        if key in self.override_choices:
            default.name = self.override_choices[key]
            default.config_name_overridden = True
            self.override_used[key] = True

    def ensure_overrides_used(self) -> None:
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


def update_package_header(
    repo: IConfigRepository,
    node: InputDefault,
    is_primary_config: bool,
) -> None:
    # This loads the same config loaded in _create_defaults_tree
    # To avoid loading it twice, the repo implementation is expected to cache
    # loaded configs
    loaded = repo.load_config(
        config_path=node.get_config_path(), is_primary_config=is_primary_config
    )
    if loaded is not None and "orig_package" in loaded.header:
        node.set_package_header(loaded.header["orig_package"])


def _expand_virtual_root(
    repo: IConfigRepository,
    root: DefaultsTreeNode,
    overrides: Overrides,
) -> DefaultsTreeNode:
    children: List[Union[DefaultsTreeNode, InputDefault]] = []
    assert root.children is not None

    for gd in overrides.append_group_defaults:
        root.children.append(gd)

    for d in reversed(root.children):
        new_root = DefaultsTreeNode(node=d, parent=root)
        d.parent_base_dir = ""
        d.parent_package = ""

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
        root.children = list(reversed(children))

    return root


def _create_defaults_tree(
    repo: IConfigRepository,
    root: DefaultsTreeNode,
    is_primary_config: bool,
    overrides: Overrides,
) -> DefaultsTreeNode:
    parent = root.node
    children: List[Union[InputDefault, DefaultsTreeNode]] = []
    if parent.is_virtual():
        return _expand_virtual_root(repo, root, overrides)
    else:
        if is_primary_config:
            root.node.parent_base_dir = ""
            root.node.parent_package = ""

        update_package_header(
            repo=repo, node=parent, is_primary_config=is_primary_config
        )

        if overrides.is_overridden(parent):
            assert isinstance(parent, GroupDefault)
            overrides.override_default_option(parent)
            # clear package header and obtain updated one from overridden config
            # (for the rare case it has changed)
            parent.package_header = None
            update_package_header(
                repo=repo, node=parent, is_primary_config=is_primary_config
            )

        path = parent.get_config_path()

        loaded = repo.load_config(config_path=path, is_primary_config=is_primary_config)

        if loaded is None:
            missing_config_error(repo, root.node)

        assert loaded is not None
        defaults_list = copy.deepcopy(loaded.new_defaults_list)

        if is_primary_config:
            for gd in overrides.append_group_defaults:
                defaults_list.append(gd)

        if len(defaults_list) > 0:
            _validate_self(containing_node=parent, defaults=defaults_list)

        for d in defaults_list:
            if d.is_self():
                continue
            d.parent_base_dir = parent.get_group_path()
            d.parent_package = parent.get_final_package()

            if isinstance(d, GroupDefault):
                assert d.group is not None
                is_legacy_hydra_override = not d.override and d.group.startswith(
                    "hydra/"
                )
                if is_legacy_hydra_override:
                    d.override = True
                    url = "https://hydra.cc/docs/next/upgrades/1.0_to_1.1/default_list_override"
                    msg = dedent(
                        f"""\
                        Default list overrides now requires 'override: true', see {url} for more information.
                        """
                    )
                    warnings.warn(msg, UserWarning)

                if d.override:
                    overrides.add_override(d)

        for d in reversed(defaults_list):
            if d.is_self():
                d.parent_base_dir = root.node.parent_base_dir
                d.parent_package = root.node.get_package()
                children.append(d)
            else:
                if isinstance(d, GroupDefault) and d.override:
                    continue
                new_root = DefaultsTreeNode(node=d, parent=root)
                d.parent_base_dir = parent.get_group_path()
                d.parent_package = parent.get_final_package()

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
        root.children = list(reversed(children))

    return root


def _create_result_default(
    tree: Optional[DefaultsTreeNode], node: InputDefault
) -> ResultDefault:
    res = ResultDefault()
    if node.is_self():
        assert tree is not None
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
) -> None:
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


def _create_root(config_name: str, with_hydra: bool) -> DefaultsTreeNode:
    if with_hydra:
        root = DefaultsTreeNode(
            node=VirtualRoot(),
            children=[
                ConfigDefault(path="hydra/config"),
                ConfigDefault(path=config_name),
            ],
        )
    else:
        root = DefaultsTreeNode(node=ConfigDefault(path=config_name))
    return root


def _create_defaults_list(
    repo: IConfigRepository,
    config_name: str,
    overrides: Overrides,
    prepend_hydra: bool,
) -> List[ResultDefault]:

    root = _create_root(config_name=config_name, with_hydra=prepend_hydra)

    defaults_tree = _create_defaults_tree(
        repo=repo,
        root=root,
        overrides=overrides,
        is_primary_config=True,
    )

    output: List[ResultDefault] = []
    _tree_to_list(tree=defaults_tree, output=output)
    # TODO: fail if duplicate items exists
    return output


def create_defaults_list(
    repo: IConfigRepository,
    config_name: str,
    overrides_list: List[Override],
    prepend_hydra: bool,
) -> DefaultsList:
    overrides = Overrides(repo=repo, overrides_list=overrides_list)
    defaults = _create_defaults_list(
        repo, config_name, overrides, prepend_hydra=prepend_hydra
    )
    overrides.ensure_overrides_used()
    ret = DefaultsList(defaults=defaults, config_overrides=overrides.config_overrides)
    return ret


# TODO: show parent config name in the error (where is my error?)
def missing_config_error(repo: IConfigRepository, element: InputDefault) -> None:
    options = None
    if isinstance(element, GroupDefault):
        group = element.get_group_path()
        options = repo.get_group_options(group, ObjectType.CONFIG)
        opt_list = "\n".join(["\t" + x for x in options])
        msg = (
            f"Could not find '{element.name}' in the config group '{group}'"
            f"\nAvailable options:\n{opt_list}\n"
        )
    else:
        msg = dedent(
            f"""\
        Could not load '{element.get_config_path()}'.
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
