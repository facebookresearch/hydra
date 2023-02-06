# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import copy
import os
import warnings
from dataclasses import dataclass, field
from textwrap import dedent
from typing import Callable, Dict, List, Optional, Set, Tuple, Union

from omegaconf import DictConfig, OmegaConf

from hydra import MissingConfigException, version
from hydra._internal.config_repository import IConfigRepository
from hydra.core.config_store import ConfigStore
from hydra.core.default_element import (
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

from .deprecation_warning import deprecation_warning

cs = ConfigStore.instance()

cs.store(name="_dummy_empty_config_", node={}, provider="hydra")


@dataclass
class Deletion:
    name: Optional[str]
    used: bool = field(default=False, compare=False)


@dataclass
class OverrideMetadata:
    external_override: bool
    containing_config_path: Optional[str] = None
    used: bool = False
    relative_key: Optional[str] = None


@dataclass
class Overrides:
    override_choices: Dict[str, Optional[Union[str, List[str]]]]
    override_metadata: Dict[str, OverrideMetadata]

    append_group_defaults: List[GroupDefault]
    config_overrides: List[Override]

    known_choices: Dict[str, Optional[str]]
    known_choices_per_group: Dict[str, Set[str]]

    deletions: Dict[str, Deletion]

    def __init__(self, repo: IConfigRepository, overrides_list: List[Override]) -> None:
        self.override_choices = {}
        self.override_metadata = {}
        self.append_group_defaults = []
        self.config_overrides = []
        self.deletions = {}

        self.known_choices = {}
        self.known_choices_per_group = {}

        for override in overrides_list:
            if override.is_sweep_override():
                continue
            is_group = repo.group_exists(override.key_or_group)
            value = override.value()
            is_dict = isinstance(override.value(), dict)
            if is_dict or not is_group:
                self.config_overrides.append(override)
            elif override.is_force_add():
                # This could probably be made to work if there is a compelling use case.
                raise ConfigCompositionException(
                    f"force-add of config groups is not supported: '{override.input_line}'"
                )
            elif override.is_delete():
                key = override.get_key_element()[1:]
                value = override.value()
                if value is not None and not isinstance(value, str):
                    raise ValueError(
                        f"Config group override deletion value must be a string : {override}"
                    )

                self.deletions[key] = Deletion(name=value)

            elif not isinstance(value, (str, list)):
                raise ValueError(
                    f"Config group override must be a string or a list. Got {type(value).__name__}"
                )
            elif override.is_add():
                self.append_group_defaults.append(
                    GroupDefault(
                        group=override.key_or_group,
                        package=override.package,
                        value=value,
                        external_append=True,
                    )
                )
            else:
                key = override.get_key_element()
                self.override_choices[key] = value
                self.override_metadata[key] = OverrideMetadata(external_override=True)

    def add_override(self, parent_config_path: str, default: GroupDefault) -> None:
        assert default.override
        key = default.get_override_key()
        if key not in self.override_choices:
            self.override_choices[key] = default.value
            self.override_metadata[key] = OverrideMetadata(
                external_override=False,
                containing_config_path=parent_config_path,
                relative_key=default.get_relative_override_key(),
            )

    def is_overridden(self, default: InputDefault) -> bool:
        if isinstance(default, GroupDefault):
            return default.get_override_key() in self.override_choices

        return False

    def override_default_option(self, default: GroupDefault) -> None:
        key = default.get_override_key()
        if key in self.override_choices:
            if isinstance(default, GroupDefault):
                default.value = self.override_choices[key]
            default.config_name_overridden = True
            self.override_metadata[key].used = True

    def ensure_overrides_used(self) -> None:
        for key, meta in self.override_metadata.items():
            if not meta.used:
                group = key.split("@")[0]
                choices = (
                    self.known_choices_per_group[group]
                    if group in self.known_choices_per_group
                    else set()
                )

                if len(choices) > 1:
                    msg = (
                        f"Could not override '{key}'."
                        f"\nDid you mean to override one of {', '.join(sorted(list(choices)))}?"
                    )
                elif len(choices) == 1:
                    msg = (
                        f"Could not override '{key}'."
                        f"\nDid you mean to override {copy.copy(choices).pop()}?"
                    )
                elif len(choices) == 0:
                    msg = f"Could not override '{key}'. No match in the defaults list."
                else:
                    assert False

                if meta.containing_config_path is not None:
                    msg = f"In '{meta.containing_config_path}': {msg}"

                if meta.external_override:
                    msg += f"\nTo append to your default list use +{key}={self.override_choices[key]}"

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
                    raise ConfigCompositionException(
                        f"Multiple values for {key}."
                        f" To override a value use 'override {key}: {prev}'"
                    )

            group = default.get_group_path()
            if group not in self.known_choices_per_group:
                self.known_choices_per_group[group] = set()
            self.known_choices_per_group[group].add(key)

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
    defaults_tree: DefaultsTreeNode
    config_overrides: List[Override]
    overrides: Overrides


def _validate_self(
    containing_node: InputDefault,
    defaults: List[InputDefault],
    has_config_content: bool,
) -> bool:
    # check that self is present only once
    has_self = False
    has_non_override = False
    for d in defaults:
        if not d.is_override():
            has_non_override = True
        if d.is_self():
            if has_self:
                raise ConfigCompositionException(
                    f"Duplicate _self_ defined in {containing_node.get_config_path()}"
                )
            has_self = True

    if not has_self and has_non_override or len(defaults) == 0:
        # This check is here to make the migration from Hydra 1.0 to Hydra 1.1 smoother and should be removed in 1.2
        # The warning should be removed in 1.2
        if containing_node.primary and has_config_content and has_non_override:
            msg = (
                f"In '{containing_node.get_config_path()}': Defaults list is missing `_self_`. "
                f"See https://hydra.cc/docs/1.2/upgrades/1.0_to_1.1/default_composition_order for more information"
            )
            if os.environ.get("SELF_WARNING_AS_ERROR") == "1":
                raise ConfigCompositionException(msg)
            warnings.warn(msg, UserWarning)
        defaults.append(ConfigDefault(path="_self_"))

    return not has_self


def update_package_header(repo: IConfigRepository, node: InputDefault) -> None:
    if node.is_missing():
        return
    # This loads the same config loaded in _create_defaults_tree
    # To avoid loading it twice, the repo implementation is expected to cache loaded configs
    loaded = repo.load_config(config_path=node.get_config_path())
    if loaded is not None:
        node.set_package_header(loaded.header["package"])


def _expand_virtual_root(
    repo: IConfigRepository,
    root: DefaultsTreeNode,
    overrides: Overrides,
    skip_missing: bool,
) -> DefaultsTreeNode:
    children: List[Union[DefaultsTreeNode, InputDefault]] = []
    assert root.children is not None
    for d in reversed(root.children):
        assert isinstance(d, InputDefault)
        new_root = DefaultsTreeNode(node=d, parent=root)
        d.update_parent("", "")

        subtree = _create_defaults_tree_impl(
            repo=repo,
            root=new_root,
            is_root_config=d.primary,
            skip_missing=skip_missing,
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
            override_key = default.get_override_key()
            options = repo.get_group_options(
                group_path,
                results_filter=ObjectType.CONFIG,
            )
            opt_list = "\n".join(["\t" + x for x in options])
            msg = dedent(
                f"""\
                You must specify '{override_key}', e.g, {override_key}=<OPTION>
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
            known_choices.defaults.append({d.get_override_key(): d.value})
    return known_choices


def _create_defaults_tree(
    repo: IConfigRepository,
    root: DefaultsTreeNode,
    is_root_config: bool,
    skip_missing: bool,
    interpolated_subtree: bool,
    overrides: Overrides,
) -> DefaultsTreeNode:
    ret = _create_defaults_tree_impl(
        repo=repo,
        root=root,
        is_root_config=is_root_config,
        skip_missing=skip_missing,
        interpolated_subtree=interpolated_subtree,
        overrides=overrides,
    )

    return ret


def _update_overrides(
    defaults_list: List[InputDefault],
    overrides: Overrides,
    parent: InputDefault,
    interpolated_subtree: bool,
) -> None:
    seen_override = False
    last_override_seen = None
    for d in defaults_list:
        if d.is_self():
            continue
        d.update_parent(parent.get_group_path(), parent.get_final_package())

        legacy_hydra_override = False
        if isinstance(d, GroupDefault):
            assert d.group is not None
            if not version.base_at_least("1.2"):
                legacy_hydra_override = not d.is_override() and d.group.startswith(
                    "hydra/"
                )

        if seen_override and not (
            d.is_override() or d.is_external_append() or legacy_hydra_override
        ):
            assert isinstance(last_override_seen, GroupDefault)
            pcp = parent.get_config_path()
            okey = last_override_seen.get_override_key()
            oval = last_override_seen.get_name()
            raise ConfigCompositionException(
                dedent(
                    f"""\
                    In {pcp}: Override '{okey} : {oval}' is defined before '{d.get_override_key()}: {d.get_name()}'.
                    Overrides must be at the end of the defaults list"""
                )
            )

        if isinstance(d, GroupDefault):
            if legacy_hydra_override:
                d.override = True
                url = "https://hydra.cc/docs/1.2/upgrades/1.0_to_1.1/defaults_list_override"
                msg = dedent(
                    f"""\
                    In {parent.get_config_path()}: Invalid overriding of {d.group}:
                    Default list overrides requires 'override' keyword.
                    See {url} for more information.
                    """
                )
                deprecation_warning(msg)

            if d.override:
                if not legacy_hydra_override:
                    seen_override = True
                last_override_seen = d
                if interpolated_subtree:
                    # Since interpolations are deferred for until all the config groups are already set,
                    # Their subtree may not contain config group overrides
                    raise ConfigCompositionException(
                        dedent(
                            f"""\
                            {parent.get_config_path()}: Default List Overrides are not allowed in the subtree
                            of an in interpolated config group (override {d.get_override_key()}={d.get_name()}).
                            """
                        )
                    )
                overrides.add_override(parent.get_config_path(), d)


def _has_config_content(cfg: DictConfig) -> bool:
    if cfg._is_none() or cfg._is_missing():
        return False

    for key in cfg.keys():
        if not OmegaConf.is_missing(cfg, key) and key != "defaults":
            return True
    return False


def _create_defaults_tree_impl(
    repo: IConfigRepository,
    root: DefaultsTreeNode,
    is_root_config: bool,
    skip_missing: bool,
    interpolated_subtree: bool,
    overrides: Overrides,
) -> DefaultsTreeNode:
    parent = root.node
    children: List[Union[InputDefault, DefaultsTreeNode]] = []
    if parent.is_virtual():
        if is_root_config:
            return _expand_virtual_root(repo, root, overrides, skip_missing)
        else:
            return root

    if is_root_config:
        root.node.update_parent("", "")
        if not repo.config_exists(root.node.get_config_path()):
            config_not_found_error(repo=repo, tree=root)

    update_package_header(repo=repo, node=parent)

    if overrides.is_deleted(parent):
        overrides.delete(parent)
        return root

    overrides.set_known_choice(parent)

    if parent.get_name() is None:
        return root

    if _check_not_missing(repo=repo, default=parent, skip_missing=skip_missing):
        return root

    path = parent.get_config_path()
    loaded = repo.load_config(config_path=path)

    if loaded is None:
        if parent.is_optional():
            assert isinstance(parent, (GroupDefault, ConfigDefault))
            parent.deleted = True
            return root
        config_not_found_error(repo=repo, tree=root)

    assert loaded is not None
    defaults_list = copy.deepcopy(loaded.defaults_list)
    if defaults_list is None:
        defaults_list = []

    self_added = False
    if (
        len(defaults_list) > 0
        or is_root_config
        and len(overrides.append_group_defaults) > 0
    ):
        has_config_content = isinstance(
            loaded.config, DictConfig
        ) and _has_config_content(loaded.config)

        self_added = _validate_self(
            containing_node=parent,
            defaults=defaults_list,
            has_config_content=has_config_content,
        )

    if is_root_config:
        defaults_list.extend(overrides.append_group_defaults)

    _update_overrides(defaults_list, overrides, parent, interpolated_subtree)

    def add_child(
        child_list: List[Union[InputDefault, DefaultsTreeNode]],
        new_root_: DefaultsTreeNode,
    ) -> None:
        subtree_ = _create_defaults_tree_impl(
            repo=repo,
            root=new_root_,
            is_root_config=False,
            interpolated_subtree=interpolated_subtree,
            skip_missing=skip_missing,
            overrides=overrides,
        )
        if subtree_.children is None:
            child_list.append(new_root_.node)
        else:
            child_list.append(subtree_)

    for d in reversed(defaults_list):
        if d.is_self():
            d.update_parent(root.node.parent_base_dir, root.node.get_package())
            children.append(d)
        else:
            if d.is_override():
                continue

            d.update_parent(parent.get_group_path(), parent.get_final_package())

            if overrides.is_overridden(d):
                assert isinstance(d, GroupDefault)
                overrides.override_default_option(d)

            if isinstance(d, GroupDefault) and d.is_options():
                # overriding may change from options to name
                for item in reversed(d.get_options()):
                    if "${" in item:
                        raise ConfigCompositionException(
                            f"In '{path}': Defaults List interpolation is not supported in options list items"
                        )

                    assert d.group is not None
                    node = ConfigDefault(
                        path=d.group + "/" + item,
                        package=d.package,
                        optional=d.is_optional(),
                    )
                    node.update_parent(
                        parent.get_group_path(), parent.get_final_package()
                    )
                    new_root = DefaultsTreeNode(node=node, parent=root)
                    add_child(children, new_root)

            else:
                if d.is_interpolation():
                    children.append(d)
                    continue

                new_root = DefaultsTreeNode(node=d, parent=root)
                add_child(children, new_root)

    # processed deferred interpolations
    known_choices = _create_interpolation_map(overrides, defaults_list, self_added)

    for idx, dd in enumerate(children):
        if isinstance(dd, InputDefault) and dd.is_interpolation():
            dd.resolve_interpolation(known_choices)
            new_root = DefaultsTreeNode(node=dd, parent=root)
            dd.update_parent(parent.get_group_path(), parent.get_final_package())
            subtree = _create_defaults_tree_impl(
                repo=repo,
                root=new_root,
                is_root_config=False,
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
    if node.is_virtual():
        return None
    if node.get_name() is None:
        return None

    res = ResultDefault()

    if node.is_self():
        assert tree is not None
        res.config_path = tree.node.get_config_path()
        res.is_self = True
        pn = tree.parent_node()
        if pn is not None:
            res.parent = pn.get_config_path()
        else:
            res.parent = None
        res.package = tree.node.get_final_package()
        res.primary = tree.node.primary
    else:
        res.config_path = node.get_config_path()
        if tree is not None:
            res.parent = tree.node.get_config_path()
        res.package = node.get_final_package()
        if isinstance(node, GroupDefault):
            res.override_key = node.get_override_key()
        res.primary = node.primary

    if res.config_path == "_dummy_empty_config_":
        return None

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

            if node.is_missing():
                return

            rd = _create_result_default(tree=tree_node, node=node)
            if rd is not None:
                self.output.append(rd)

    visitor = Collector()
    _dfs_walk(tree, visitor)
    return visitor.output


def _create_root(config_name: Optional[str], with_hydra: bool) -> DefaultsTreeNode:
    primary: InputDefault
    if config_name is None:
        primary = ConfigDefault(path="_dummy_empty_config_", primary=True)
    else:
        primary = ConfigDefault(path=config_name, primary=True)

    if with_hydra:
        root = DefaultsTreeNode(
            node=VirtualRoot(),
            children=[ConfigDefault(path="hydra/config"), primary],
        )
    else:
        root = DefaultsTreeNode(node=primary)
    return root


def ensure_no_duplicates_in_list(result: List[ResultDefault]) -> None:
    keys = set()
    for item in result:
        if not item.is_self:
            key = item.override_key
            if key is not None:
                if key in keys:
                    raise ConfigCompositionException(
                        f"{key} appears more than once in the final defaults list"
                    )
                keys.add(key)


def _create_defaults_list(
    repo: IConfigRepository,
    config_name: Optional[str],
    overrides: Overrides,
    prepend_hydra: bool,
    skip_missing: bool,
) -> Tuple[List[ResultDefault], DefaultsTreeNode]:
    root = _create_root(config_name=config_name, with_hydra=prepend_hydra)

    defaults_tree = _create_defaults_tree(
        repo=repo,
        root=root,
        overrides=overrides,
        is_root_config=True,
        interpolated_subtree=False,
        skip_missing=skip_missing,
    )

    output = _tree_to_list(tree=defaults_tree)
    ensure_no_duplicates_in_list(output)
    return output, defaults_tree


def create_defaults_list(
    repo: IConfigRepository,
    config_name: Optional[str],
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
    defaults, tree = _create_defaults_list(
        repo,
        config_name,
        overrides,
        prepend_hydra=prepend_hydra,
        skip_missing=skip_missing,
    )
    overrides.ensure_overrides_used()
    overrides.ensure_deletions_used()
    return DefaultsList(
        defaults=defaults,
        config_overrides=overrides.config_overrides,
        defaults_tree=tree,
        overrides=overrides,
    )


def config_not_found_error(repo: IConfigRepository, tree: DefaultsTreeNode) -> None:
    element = tree.node
    options = None
    group = None
    if isinstance(element, GroupDefault):
        group = element.get_group_path()
        options = repo.get_group_options(group, ObjectType.CONFIG)

    if element.primary:
        msg = dedent(
            f"""\
        Cannot find primary config '{element.get_config_path()}'. Check that it's in your config search path.
        """
        )
    else:
        parent = tree.parent.node if tree.parent is not None else None
        if isinstance(element, GroupDefault):
            msg = f"Could not find '{element.get_config_path()}'\n"
            if options is not None and len(options) > 0:
                opt_list = "\n".join(["\t" + x for x in options])
                msg = f"{msg}\nAvailable options in '{group}':\n" + opt_list
        else:
            msg = dedent(
                f"""\
            Could not load '{element.get_config_path()}'.
            """
            )

        if parent is not None:
            msg = f"In '{parent.get_config_path()}': {msg}"

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
