# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import re
import zipfile
from typing import Any, List

from pytest import mark, param, raises

from hydra._internal.config_repository import ConfigRepository
from hydra._internal.config_search_path_impl import ConfigSearchPathImpl
from hydra._internal.core_plugins.file_config_source import FileConfigSource
from hydra._internal.core_plugins.importlib_resources_config_source import (
    ImportlibResourcesConfigSource,
)
from hydra._internal.core_plugins.structured_config_source import StructuredConfigSource
from hydra.core.default_element import GroupDefault, InputDefault
from hydra.core.plugins import Plugins
from hydra.core.singleton import Singleton
from hydra.plugins.config_source import ConfigSource
from hydra.test_utils.config_source_common_tests import ConfigSourceTestSuite
from hydra.test_utils.test_utils import chdir_hydra_root

chdir_hydra_root()


# Manually save and restore singletons to work around an issue with things added to the config store via importing.
# restoring is done in test_restore_singleton_state_hack(), which must be the last test in this file.
state = copy.deepcopy(Singleton.get_state())


@mark.parametrize(
    "type_, path",
    [
        param(
            FileConfigSource,
            "file://tests/test_apps/config_source_test/dir",
            id="FileConfigSource",
        ),
        param(
            ImportlibResourcesConfigSource,
            "pkg://tests.test_apps.config_source_test.dir",
            id="ImportlibResourcesConfigSource",
        ),
        param(
            StructuredConfigSource,
            "structured://tests.test_apps.config_source_test.structured",
            id="StructuredConfigSource",
        ),
    ],
)
class TestCoreConfigSources(ConfigSourceTestSuite):
    pass


def create_config_search_path(path: str) -> ConfigSearchPathImpl:
    csp = ConfigSearchPathImpl()
    csp.append(provider="test", path=path)
    return csp


@mark.parametrize(
    "path",
    [
        "file://tests/test_apps/config_source_test/dir",
        "pkg://tests.test_apps.config_source_test.dir",
    ],
)
class TestConfigRepository:
    def test_config_repository_load(
        self, hydra_restore_singletons: Any, path: str
    ) -> None:
        Plugins.instance()  # initializes
        config_search_path = create_config_search_path(path)
        repo = ConfigRepository(config_search_path=config_search_path)
        ret = repo.load_config(config_path="dataset/imagenet.yaml")
        assert ret is not None
        assert ret.config == {"name": "imagenet", "path": "/datasets/imagenet"}
        assert repo.load_config(config_path="not_found.yaml") is None

    def test_config_repository_exists(
        self, hydra_restore_singletons: Any, path: str
    ) -> None:
        Plugins.instance()  # initializes
        config_search_path = create_config_search_path(path)
        repo = ConfigRepository(config_search_path=config_search_path)
        assert repo.config_exists("dataset/imagenet.yaml")
        assert not repo.config_exists("not_found.yaml")

    @mark.parametrize(
        "config_path,expected",
        [
            param(
                "primary_config",
                [],
                id="no_defaults",
            ),
            param(
                "config_with_defaults_list",
                [GroupDefault(group="dataset", value="imagenet")],
                id="defaults_in_root",
            ),
            param(
                "configs_with_defaults_list/global_package",
                [GroupDefault(group="foo", value="bar")],
                id="configs_with_defaults_list/global_package",
            ),
            param(
                "configs_with_defaults_list/group_package",
                [GroupDefault(group="foo", value="bar")],
                id="configs_with_defaults_list/group_package",
            ),
            param(
                "configs_with_defaults_list/no_package",
                [GroupDefault(group="foo", value="bar")],
                id="configs_with_defaults_list/no_package",
            ),
        ],
    )
    def test_config_repository_list(
        self,
        hydra_restore_singletons: Any,
        path: str,
        config_path: str,
        expected: List[InputDefault],
    ) -> None:
        Plugins.instance()
        config_search_path = create_config_search_path(path)
        repo = ConfigRepository(config_search_path=config_search_path)
        ret = repo.load_config(config_path)
        assert ret is not None
        assert ret.defaults_list == expected


@mark.parametrize("sep", [" "])
@mark.parametrize(
    "cfg_text, expected",
    [
        ("# @package{sep}foo.bar", {"package": "foo.bar"}),
        ("# @package{sep} foo.bar", {"package": "foo.bar"}),
        ("# @package {sep}foo.bar", {"package": "foo.bar"}),
        ("#@package{sep}foo.bar", {"package": "foo.bar"}),
        ("#@package{sep}foo.bar ", {"package": "foo.bar"}),
        (
            "#@package{sep}foo.bar bah",
            raises(ValueError, match=re.escape("Too many components in")),
        ),
        (
            "#@package",
            raises(
                ValueError, match=re.escape("Expected header format: KEY VALUE, got")
            ),
        ),
        (
            """# @package{sep}foo.bar
foo: bar
# comment dsa
""",
            {"package": "foo.bar"},
        ),
        (
            """
# @package{sep}foo.bar
""",
            {"package": "foo.bar"},
        ),
    ],
)
def test_get_config_header(cfg_text: str, expected: Any, sep: str) -> None:
    cfg_text = cfg_text.format(sep=sep)
    if isinstance(expected, dict):
        header = ConfigSource._get_header_dict(cfg_text)
        assert header == expected
    else:
        with expected:
            ConfigSource._get_header_dict(cfg_text)


def test_singleton_get_state(hydra_restore_singletons: Any) -> None:
    s = Singleton.get_state()
    assert Plugins not in s["instances"]
    assert Plugins in Singleton._instances
    Singleton.set_state(s)
    assert Plugins in Singleton._instances


def test_restore_singleton_state_hack() -> None:
    """
    This is a hack that allow us to undo changes to the ConfigStore.
    During this test, the config store is being modified in Python imports.
    Python imports can only run once, so clearing the state during the tests will break
    The tests because it will not be reinitialized.

    A solution is to undo the changes after the last test.
    The reason this logic is in a test is that if it's outside it's being executed during
    Pytest's test collection phase, which is before the tests are dunning - so it does not solve the problem.
    """
    Singleton.set_state(state)


def test_importlib_resource_load_zip_path() -> None:
    config_source = ImportlibResourcesConfigSource(provider="foo", path="pkg://bar")
    conf = config_source._read_config(
        zipfile.Path("hydra/test_utils/configs/conf.zip", "config.yaml")
    )
    assert conf.config == {"foo": "bar"}
    assert conf.header == {"package": None}
