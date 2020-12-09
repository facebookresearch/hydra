# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
from dataclasses import dataclass
from itertools import filterfalse
from textwrap import dedent
from typing import Dict, List, Optional, Union

from omegaconf import II, DictConfig, OmegaConf

from hydra._internal.config_repository import IConfigRepository
from hydra.core import DefaultElement
from hydra.core.object_type import ObjectType
from hydra.core.override_parser.types import Override
from hydra.errors import ConfigCompositionException, MissingConfigException


@dataclass(frozen=True, eq=True)
class DeleteKey:
    fqgn: str
    config_name: Optional[str]
    must_delete: bool

    def __repr__(self) -> str:
        if self.config_name is None:
            return self.fqgn
        else:
            return f"{self.fqgn}={self.config_name}"


@dataclass
class DefaultsList:
    original: List[DefaultElement]
    effective: List[DefaultElement]


def compute_element_defaults_list(
    element: DefaultElement,
    repo: IConfigRepository,
    skip_missing: bool,
) -> List[DefaultElement]:
    group_to_choice = OmegaConf.create({})
    delete_groups: Dict[DeleteKey, int] = {}
    ret = _compute_element_defaults_list_impl(
        element=element,
        group_to_choice=group_to_choice,
        delete_groups=delete_groups,
        skip_missing=skip_missing,
        repo=repo,
    )

    _post_process_deletes(ret, delete_groups)
    return ret


def _post_process_deletes(
    ret: List[DefaultElement],
    delete_groups: Dict[DeleteKey, int],
) -> None:
    # verify all deletions deleted something
    for g, c in delete_groups.items():
        if c == 0 and g.must_delete:
            raise ConfigCompositionException(
                f"Could not delete. No match for '{g}' in the defaults list."
            )

    # remove delete overrides
    ret[:] = filterfalse(lambda x: x.is_delete, ret)


def expand_defaults_list(
    defaults: List[DefaultElement],
    skip_missing: bool,
    repo: IConfigRepository,
) -> List[DefaultElement]:
    return _expand_defaults_list(
        self_element=None,
        defaults=defaults,
        skip_missing=skip_missing,
        repo=repo,
    )


def _update_known_state(
    d: DefaultElement,
    group_to_choice: DictConfig,
    delete_groups: Dict[DeleteKey, int],
) -> None:
    fqgn = d.fully_qualified_group_name()
    if fqgn is None:
        return

    is_overridden = fqgn in group_to_choice

    if d.config_group is not None:
        if (
            fqgn not in group_to_choice
            and not d.is_delete
            and d.config_name not in ("_self_", "_keep_")
            and not is_matching_deletion(delete_groups=delete_groups, d=d)
        ):
            group_to_choice[fqgn] = d.config_name

    if d.is_delete:
        if is_overridden:
            d.is_delete = False
            d.config_name = group_to_choice[fqgn]
        else:
            delete_key = DeleteKey(
                fqgn,
                d.config_name if d.config_name != "_delete_" else None,
                must_delete=d.from_override,
            )
            if delete_key not in delete_groups:
                delete_groups[delete_key] = 0


def _expand_defaults_list(
    self_element: Optional[DefaultElement],
    defaults: List[DefaultElement],
    skip_missing: bool,
    repo: IConfigRepository,
) -> List[DefaultElement]:
    group_to_choice = OmegaConf.create({})
    delete_groups: Dict[DeleteKey, int] = {}
    for d in reversed(defaults):
        _update_known_state(
            d,
            group_to_choice=group_to_choice,
            delete_groups=delete_groups,
        )

    dl = DefaultsList(
        original=copy.deepcopy(defaults),
        effective=copy.deepcopy(defaults),
    )
    ret = _expand_defaults_list_impl(
        self_element=self_element,
        defaults_list=dl,
        group_to_choice=group_to_choice,
        delete_groups=delete_groups,
        skip_missing=skip_missing,
        repo=repo,
    )

    _post_process_deletes(ret, delete_groups)

    return ret


def _validate_self(element: DefaultElement, defaults: DefaultsList) -> None:
    # check that self is present only once
    has_self = False
    for d in defaults.effective:
        if d.config_name == "_self_":
            if has_self is True:
                raise ConfigCompositionException(
                    f"Duplicate _self_ defined in {element.config_path()}"
                )
            has_self = True
            assert d.config_group is None
            d.config_group = element.config_group
            d.package = element.package
            d.parent = element.parent

    if not has_self:
        me = copy.deepcopy(element)
        me.config_name = "_self_"
        me.from_override = False
        me.parent = element.parent
        defaults.effective.insert(0, me)


def _compute_element_defaults_list_impl(
    element: DefaultElement,
    group_to_choice: DictConfig,
    delete_groups: Dict[DeleteKey, int],
    skip_missing: bool,
    repo: IConfigRepository,
) -> List[DefaultElement]:
    deleted = delete_if_matching(delete_groups, element)
    if deleted:
        return []

    if element.config_name == "???":
        if skip_missing:
            element.set_skip_load("missing_skipped")
            return [element]
        else:
            if element.config_group is not None:
                options = repo.get_group_options(
                    element.config_group, results_filter=ObjectType.CONFIG
                )
                opt_list = "\n".join(["\t" + x for x in options])
                msg = (
                    f"You must specify '{element.config_group}', e.g, {element.config_group}=<OPTION>"
                    f"\nAvailable options:"
                    f"\n{opt_list}"
                )
            else:
                msg = f"You must specify '{element.config_group}', e.g, {element.config_group}=<OPTION>"

            raise ConfigCompositionException(msg)

    loaded = repo.load_config(
        config_path=element.config_path(),
        is_primary_config=element.primary,
    )

    if loaded is None:
        if element.optional:
            element.set_skip_load("missing_optional_config")
            return [element]
        else:
            missing_config_error(repo=repo, element=element)
    else:
        original = copy.deepcopy(loaded.defaults_list)
        effective = copy.deepcopy(loaded.defaults_list)

    defaults = DefaultsList(original=original, effective=effective)
    _validate_self(element, defaults)

    return _expand_defaults_list_impl(
        self_element=element,
        defaults_list=defaults,
        group_to_choice=group_to_choice,
        delete_groups=delete_groups,
        skip_missing=skip_missing,
        repo=repo,
    )


def _find_match_before(
    defaults: List[DefaultElement], like: DefaultElement
) -> Optional[DefaultElement]:
    fqgn = like.fully_qualified_group_name()
    for d2 in defaults:
        if d2 == like:
            break
        if d2.fully_qualified_group_name() == fqgn:
            return d2
    return None


def _verify_no_add_conflicts(defaults: List[DefaultElement]) -> None:
    for d in reversed(defaults):
        if d.from_override and not d.skip_load and not d.is_delete:
            fqgn = d.fully_qualified_group_name()
            match = _find_match_before(defaults, d)
            if d.is_add and match is not None:
                raise ConfigCompositionException(
                    f"Could not add '{fqgn}={d.config_name}'. '{fqgn}' is already in the defaults list."
                )
            if not d.is_add and match is None:
                msg = (
                    f"Could not override '{fqgn}'. No match in the defaults list."
                    f"\nTo append to your default list use +{fqgn}={d.config_name}"
                )
                raise ConfigCompositionException(msg)


def _process_renames(defaults: List[DefaultElement]) -> None:
    while True:
        last_rename_index = -1
        for idx, d in reversed(list(enumerate(defaults))):
            if d.is_package_rename():
                last_rename_index = idx
                break
        if last_rename_index != -1:
            rename = defaults.pop(last_rename_index)
            renamed = False
            for d in defaults:
                if is_matching(rename, d):
                    d.package = rename.get_subject_package()
                    renamed = True
            if not renamed:
                raise ConfigCompositionException(
                    f"Could not rename package. "
                    f"No match for '{rename.config_group}@{rename.package}' in the defaults list"
                )
        else:
            break


def delete_if_matching(delete_groups: Dict[DeleteKey, int], d: DefaultElement) -> bool:
    return is_matching_deletion(
        delete_groups=delete_groups, d=d, mark_item_as_deleted=True
    )


def is_matching_deletion(
    delete_groups: Dict[DeleteKey, int],
    d: DefaultElement,
    mark_item_as_deleted: bool = False,
) -> bool:
    matched = False
    for delete in delete_groups:
        if delete.fqgn == d.fully_qualified_group_name():
            if delete.config_name is None:
                # fqdn only
                matched = True
                if mark_item_as_deleted:
                    delete_groups[delete] += 1
                    d.is_deleted = True
                    d.set_skip_load("deleted_from_list")
            else:
                if delete.config_name == d.config_name:
                    matched = True
                    if mark_item_as_deleted:
                        delete_groups[delete] += 1
                        d.is_deleted = True
                        d.set_skip_load("deleted_from_list")
    return matched


def _expand_defaults_list_impl(
    self_element: Optional[DefaultElement],
    defaults_list: DefaultsList,
    group_to_choice: DictConfig,
    delete_groups: Dict[DeleteKey, int],
    skip_missing: bool,
    repo: IConfigRepository,
) -> List[DefaultElement]:

    # list order is determined by first instance from that config group
    # selected config group is determined by the last override

    deferred_overrides = []
    defaults = defaults_list.effective

    ret: List[Union[DefaultElement, List[DefaultElement]]] = []
    for d in reversed(defaults):
        _update_known_state(
            d, group_to_choice=group_to_choice, delete_groups=delete_groups
        )

        fqgn = d.fully_qualified_group_name()
        if d.config_name == "_self_":
            if self_element is None:
                raise ConfigCompositionException(
                    "self_name is not specified and defaults list contains a _self_ item"
                )
            d = copy.deepcopy(d)
            # override self_name
            if fqgn is not None and fqgn in group_to_choice:
                d.config_name = group_to_choice[fqgn]
            else:
                d.config_name = self_element.config_name
            added_sublist = [d]
        elif d.is_package_rename():
            added_sublist = [d]  # defer rename
        elif d.is_delete:
            added_sublist = [d]
        elif d.from_override:
            added_sublist = [d]  # defer override processing
            deferred_overrides.append(d)
        elif d.is_interpolation():
            deferred_overrides.append(d)
            added_sublist = [d]  # defer interpolation
        else:
            if delete_if_matching(delete_groups, d):
                added_sublist = [d]
            else:
                if fqgn is not None and fqgn in group_to_choice:
                    d.config_name = group_to_choice[fqgn]
                    if d.is_delete:
                        d.is_delete = False

                added_sublist = _compute_element_defaults_list_impl(
                    element=d,
                    group_to_choice=group_to_choice,
                    delete_groups=delete_groups,
                    skip_missing=skip_missing,
                    repo=repo,
                )

        ret.append(added_sublist)

    ret.reverse()
    result: List[DefaultElement] = [item for sublist in ret for item in sublist]  # type: ignore

    _process_renames(result)

    # process deletes
    for element in reversed(result):
        if not element.is_delete:
            delete_if_matching(delete_groups, element)

    _verify_no_add_conflicts(result)

    # prepare a local group_to_choice with the defaults to support
    # legacy interpolations like ${defaults.1.a}
    # Support for this will be removed in Hydra 1.2
    group_to_choice2 = copy.deepcopy(group_to_choice)
    group_to_choice2.defaults = []
    for d in defaults_list.original:
        if d.config_group is not None:
            group_to_choice2.defaults.append({d.config_group: II(d.config_group)})
        else:
            group_to_choice2.defaults.append(d.config_name)

    deferred_overrides = deduplicate_deferred(deferred_overrides, result)

    # expand deferred
    for d in deferred_overrides:
        if d.is_interpolation():
            d.resolve_interpolation(group_to_choice2)

        item_defaults = _compute_element_defaults_list_impl(
            element=d,
            group_to_choice=group_to_choice,
            delete_groups=delete_groups,
            skip_missing=skip_missing,
            repo=repo,
        )
        index = result.index(d)
        result[index:index] = item_defaults

    dedupped_defaults = _deduplicate(result)
    return dedupped_defaults


def deduplicate_deferred(
    deferred: List[DefaultElement],
    defaults_list: List[DefaultElement],
) -> List[DefaultElement]:
    # this is a bit hacky. deferred overrides that exists in current defaults list
    # were already processed via the known state and should not be processed again
    res = []
    seen_groups = set()
    for d in defaults_list:
        if d.config_group is not None:
            seen_groups.add(d.fully_qualified_group_name())

    for de in deferred:
        if not de.from_override or de.is_add:
            res.append(de)
        else:
            if not de.fully_qualified_group_name() in seen_groups:
                res.append(de)
    return res


def _deduplicate(defaults_list: List[DefaultElement]) -> List[DefaultElement]:
    deduped = []
    seen_groups = set()
    for d in defaults_list:
        if d.config_group is not None:
            fqgn = d.fully_qualified_group_name()
            if fqgn not in seen_groups:
                seen_groups.add(fqgn)
                deduped.append(d)
        else:
            deduped.append(d)
    return deduped


def missing_config_error(repo: IConfigRepository, element: DefaultElement) -> None:
    options = None
    if element.config_group is not None:
        options = repo.get_group_options(element.config_group, ObjectType.CONFIG)
        opt_list = "\n".join(["\t" + x for x in options])
        msg = (
            f"Could not find '{element.config_name}' in the config group '{element.config_group}'"
            f"\nAvailable options:\n{opt_list}\n"
        )
    else:
        msg = dedent(
            f"""\
        Could not load {element.config_path()}.
        """
        )

    descs = []
    for src in repo.get_sources():
        descs.append(f"\t{repr(src)}")
    lines = "\n".join(descs)
    msg += "\nConfig search path:" + f"\n{lines}"

    raise MissingConfigException(
        missing_cfg_file=element.config_path(),
        message=msg,
        options=options,
    )


def is_matching(rename: DefaultElement, other: DefaultElement) -> bool:
    if rename.config_group != other.config_group:
        return False
    if rename.package == other.package:
        return True
    return False


def convert_overrides_to_defaults(
    parsed_overrides: List[Override],
) -> List[DefaultElement]:
    ret = []
    for override in parsed_overrides:
        value = override.value()
        if override.is_delete() and value is None:
            value = "_delete_"

        if not isinstance(value, str):
            raise ConfigCompositionException(
                "Defaults list supported delete syntax is in the form"
                " ~group and ~group=value, where value is a group name (string)"
            )

        default = DefaultElement(
            config_group=override.key_or_group,
            config_name=value,
            package=override.package,
            from_override=True,
            parent="overrides",
        )

        if override.is_delete():
            default.is_delete = True

        if override.is_add():
            default.is_add = True
        ret.append(default)
    return ret
