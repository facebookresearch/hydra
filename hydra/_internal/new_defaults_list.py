# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import copy
import warnings
from dataclasses import dataclass, field
from textwrap import dedent
from typing import Callable, Dict, List, Optional, Union

from omegaconf import DictConfig, OmegaConf

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
class Deletion:
    name: Optional[str]
    used: bool = field(default=False, compare=False)


@dataclass
class Overrides:
    override_choices: Dict[str, Optional[str]]
    override_used: Dict[str, bool]

    append_group_defaults: List[GroupDefault]
    config_overrides: List[Override]

    known_choices: Dict[str, Optional[str]]

    deletions: Dict[str, Deletion]

    def __init__(self, repo: IConfigRepository, overrides_list: List[Override]) -> None:
        self.override_choices = {}
        self.override_used = {}
        self.append_group_defaults = []
        self.config_overrides = []
        self.deletions = {}

        self.known_choices = {}

        for override in overrides_list:
            is_group = repo.group_exists(override.key_or_group)
            value = override.value()
            if not is_group:
                self.config_overrides.append(override)
            else:
                if override.is_delete():
                    key = override.get_key_element()[1:]
                    value = override.value()
                    if value is not None and not isinstance(value, str):
                        raise ValueError(
                            f"Config group override deletion value must be a string : {override}"
                        )

                    self.deletions[key] = Deletion(name=value)

                elif not isinstance(value, str):
                    raise ValueError(
                        f"Config group override must be a string : {override}"
                    )
                elif override.is_add():
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

    def ensure_deletions_used(self) -> None:
        for key, deletion in self.deletions.items():
            if not deletion.used:
                desc = f"{key}={deletion.name}" if deletion.name is not None else key
                msg = f"Could not delete '{desc}'. No match in the defaults list"
                raise ConfigCompositionException(msg)

    def set_known_choice(self, default: InputDefault) -> None:
        if isinstance(default, GroupDefault):
            key = default.get_override_key()
            if key not in self.known_choices:
                self.known_choices[key] = default.get_name()
            else:
                prev = self.known_choices[key]
                if default.get_name() != prev:
                    raise ValueError(
                        f"Internal error, value of {key} is being changed from {prev} to {default.get_name()}"
                    )

    def is_deleted(self, default: InputDefault) -> bool:
        if not isinstance(default, GroupDefault):
            return False
        key = default.get_override_key()
        if key in self.deletions:
            deletion = self.deletions[key]
            if deletion.name is None:
                return True
            else:
                return deletion.name == default.get_name()
        return False

    def delete(self, default: InputDefault) -> None:
        assert isinstance(default, GroupDefault)
        default.deleted = True

        key = default.get_override_key()
        self.deletions[key].used = True


@dataclass
class DefaultsList:
    defaults: List[ResultDefault]
    config_overrides: List[Override]


def _validate_self(containing_node: InputDefault, defaults: List[InputDefault]) -> bool:
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

    return not has_self


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
    assert len(root.children) == 2
    for gd in overrides.append_group_defaults:
        root.children.append(gd)

    for d in reversed(root.children):
        assert isinstance(d, InputDefault)
        new_root = DefaultsTreeNode(node=d, parent=root)
        d.parent_base_dir = ""
        d.parent_package = ""

        subtree = _create_defaults_tree_impl(
            repo=repo,
            root=new_root,
            is_primary_config=False,
            skip_missing=False,
            interpolated_subtree=False,
            overrides=overrides,
        )
        if subtree.children is None:
            children.append(d)
        else:
            children.append(subtree)

    if len(children) > 0:
        root.children = list(reversed(children))

    return root


def _check_not_missing(
    repo: IConfigRepository,
    default: InputDefault,
    skip_missing: bool,
) -> bool:
    path = default.get_config_path()
    if path.endswith("???"):
        if skip_missing:
            return True
        if isinstance(default, GroupDefault):
            group_path = default.get_group_path()
            options = repo.get_group_options(
                group_path,
                results_filter=ObjectType.CONFIG,
            )
            opt_list = "\n".join(["\t" + x for x in options])
            msg = dedent(
                f"""\
                You must specify '{group_path}', e.g, {group_path}=<OPTION>
                Available options:
                """
            )
            raise ConfigCompositionException(msg + opt_list)
        elif isinstance(default, ConfigDefault):
            raise ValueError(f"Missing ConfigDefault is not supported : {path}")
        else:
            assert False

    return False


def _create_interpolation_map(
    overrides: Overrides,
    defaults_list: List[InputDefault],
    self_added: bool,
) -> DictConfig:
    known_choices = OmegaConf.create(overrides.known_choices)
    known_choices.defaults = []
    for d in defaults_list:
        if self_added and d.is_self():
            continue
        if isinstance(d, ConfigDefault):
            known_choices.defaults.append(d.get_config_path())
        elif isinstance(d, GroupDefault):
            name = d.get_name()
            known_choices.defaults.append({d.get_override_key(): name})
    return known_choices


def _create_defaults_tree(
    repo: IConfigRepository,
    root: DefaultsTreeNode,
    is_primary_config: bool,
    skip_missing: bool,
    interpolated_subtree: bool,
    overrides: Overrides,
) -> DefaultsTreeNode:
    ret = _create_defaults_tree_impl(
        repo=repo,
        root=root,
        is_primary_config=is_primary_config,
        skip_missing=skip_missing,
        interpolated_subtree=interpolated_subtree,
        overrides=overrides,
    )

    return ret


def _create_defaults_tree_impl(
    repo: IConfigRepository,
    root: DefaultsTreeNode,
    is_primary_config: bool,
    skip_missing: bool,
    interpolated_subtree: bool,
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

        if overrides.is_deleted(parent):
            overrides.delete(parent)
            # parent.deleted = True
            return root

        overrides.set_known_choice(parent)

        if parent.get_name() is None:
            return root

        if _check_not_missing(repo=repo, default=parent, skip_missing=skip_missing):
            return root

        path = parent.get_config_path()
        loaded = repo.load_config(config_path=path, is_primary_config=is_primary_config)

        if loaded is None:
            config_not_found_error(repo, root.node)

        assert loaded is not None
        defaults_list = copy.deepcopy(loaded.new_defaults_list)

        if is_primary_config:
            for gd in overrides.append_group_defaults:
                defaults_list.append(gd)

        self_added = False
        if len(defaults_list) > 0:
            self_added = _validate_self(containing_node=parent, defaults=defaults_list)

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
                    if interpolated_subtree:
                        # Since interpolations are deferred for until all the config groups are already set,
                        # Their subtree may not contain config group overrides
                        raise ConfigCompositionException(
                            f"{parent.get_config_path()}: Overrides are not allowed in the subtree"
                            f" of an in interpolated config group ({d.get_override_key()}={d.get_name()})"
                        )
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

                if d.is_interpolation():
                    children.append(d)
                    continue

                subtree = _create_defaults_tree_impl(
                    repo=repo,
                    root=new_root,
                    is_primary_config=False,
                    interpolated_subtree=interpolated_subtree,
                    skip_missing=skip_missing,
                    overrides=overrides,
                )
                if subtree.children is None:
                    children.append(d)
                else:
                    children.append(subtree)

        # processed deferred interpolations
        known_choices = _create_interpolation_map(overrides, defaults_list, self_added)

        for idx, dd in enumerate(children):
            if isinstance(dd, InputDefault) and dd.is_interpolation():
                dd.resolve_interpolation(known_choices)
                new_root = DefaultsTreeNode(node=dd, parent=root)
                dd.parent_base_dir = parent.get_group_path()
                dd.parent_package = parent.get_final_package()
                subtree = _create_defaults_tree_impl(
                    repo=repo,
                    root=new_root,
                    is_primary_config=False,
                    skip_missing=skip_missing,
                    interpolated_subtree=True,
                    overrides=overrides,
                )
                if subtree.children is not None:
                    children[idx] = subtree

    if len(children) > 0:
        root.children = list(reversed(children))

    return root


def _create_result_default(
    tree: Optional[DefaultsTreeNode], node: InputDefault
) -> Optional[ResultDefault]:
    if node.get_name() is None:
        return None

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


def _dfs_walk(
    tree: DefaultsTreeNode,
    operator: Callable[[Optional[DefaultsTreeNode], InputDefault], None],
) -> None:
    if tree.children is None or len(tree.children) == 0:
        operator(tree.parent, tree.node)
    else:
        for child in tree.children:
            if isinstance(child, InputDefault):
                operator(tree, child)
            else:
                assert isinstance(child, DefaultsTreeNode)
                _dfs_walk(tree=child, operator=operator)


def _tree_to_list(
    tree: DefaultsTreeNode,
) -> List[ResultDefault]:
    class Collector:
        def __init__(self) -> None:
            self.output: List[ResultDefault] = []

        def __call__(
            self, tree_node: Optional[DefaultsTreeNode], node: InputDefault
        ) -> None:
            if node.is_deleted():
                return

            rd = _create_result_default(tree=tree_node, node=node)
            if rd is not None:
                self.output.append(rd)

    visitor = Collector()
    _dfs_walk(tree, visitor)
    return visitor.output


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
    skip_missing: bool,
) -> List[ResultDefault]:

    root = _create_root(config_name=config_name, with_hydra=prepend_hydra)

    defaults_tree = _create_defaults_tree(
        repo=repo,
        root=root,
        overrides=overrides,
        is_primary_config=True,
        interpolated_subtree=False,
        skip_missing=skip_missing,
    )

    output = _tree_to_list(tree=defaults_tree)
    # TODO: fail if duplicate items exists
    return output


def create_defaults_list(
    repo: IConfigRepository,
    config_name: str,
    overrides_list: List[Override],
    prepend_hydra: bool,
    skip_missing: bool,
) -> DefaultsList:
    """
    :param repo:
    :param config_name:
    :param overrides_list:
    :param prepend_hydra:
    :param skip_missing: True to skip config group with the value '???' and not fail on them. Useful when sweeping.
    :return:
    """
    overrides = Overrides(repo=repo, overrides_list=overrides_list)
    defaults = _create_defaults_list(
        repo,
        config_name,
        overrides,
        prepend_hydra=prepend_hydra,
        skip_missing=skip_missing,
    )
    overrides.ensure_overrides_used()
    overrides.ensure_deletions_used()
    ret = DefaultsList(defaults=defaults, config_overrides=overrides.config_overrides)
    return ret


# TODO: show parent config name in the error (where is my error?)
def config_not_found_error(repo: IConfigRepository, element: InputDefault) -> None:
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
