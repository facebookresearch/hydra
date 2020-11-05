# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import re
from typing import Any, List, Optional

import pytest

from hydra._internal.config_repository import ConfigRepository
from hydra._internal.config_search_path_impl import ConfigSearchPathImpl
from hydra._internal.core_plugins.file_config_source import FileConfigSource
from hydra._internal.core_plugins.importlib_resources_config_source import (
    ImportlibResourcesConfigSource,
)
from hydra._internal.core_plugins.structured_config_source import StructuredConfigSource
from hydra.core.object_type import ObjectType
from hydra.core.plugins import Plugins
from hydra.plugins.config_source import ConfigSource
from hydra.test_utils.config_source_common_tests import ConfigSourceTestSuite
from hydra.test_utils.test_utils import chdir_hydra_root

chdir_hydra_root()


@pytest.mark.parametrize(
    "type_, path",
    [
        pytest.param(
            FileConfigSource,
            "file://tests/test_apps/config_source_test/dir",
            id="FileConfigSource",
        ),
        pytest.param(
            ImportlibResourcesConfigSource,
            "pkg://tests.test_apps.config_source_test.dir",
            id="ImportlibResourcesConfigSource",
        ),
        pytest.param(
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


@pytest.mark.parametrize(
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
        ret = repo.load_config(
            config_path="dataset/imagenet.yaml", is_primary_config=False
        )
        assert ret is not None
        assert ret.config == {
            "dataset": {"name": "imagenet", "path": "/datasets/imagenet"}
        }
        assert (
            repo.load_config(config_path="not_found.yaml", is_primary_config=True)
            is None
        )

    def test_config_repository_exists(
        self, hydra_restore_singletons: Any, path: str
    ) -> None:
        Plugins.instance()  # initializes
        config_search_path = create_config_search_path(path)
        repo = ConfigRepository(config_search_path=config_search_path)
        assert repo.config_exists("dataset/imagenet.yaml")
        assert not repo.config_exists("not_found.yaml")

    @pytest.mark.parametrize(  # type: ignore
        "config_path,results_filter,expected",
        [
            pytest.param(
                "",
                None,
                [
                    "config_with_defaults_list",
                    "config_with_unicode",
                    "config_without_group",
                    "configs_with_defaults_list",
                    "dataset",
                    "level1",
                    "optimizer",
                    "package_test",
                    "primary_config",
                    "primary_config_with_non_global_package",
                ],
                id="root:no_filter",
            ),
            pytest.param(
                "",
                ObjectType.GROUP,
                [
                    "configs_with_defaults_list",
                    "dataset",
                    "level1",
                    "optimizer",
                    "package_test",
                ],
                id="root:group",
            ),
            pytest.param(
                "",
                ObjectType.CONFIG,
                [
                    "config_with_defaults_list",
                    "config_with_unicode",
                    "config_without_group",
                    "dataset",
                    "primary_config",
                    "primary_config_with_non_global_package",
                ],
                id="root:config",
            ),
            pytest.param(
                "dataset",
                None,
                ["cifar10", "imagenet"],
                id="dataset:no_filter",
            ),
            pytest.param("dataset", ObjectType.GROUP, [], id="dataset:group"),
            pytest.param(
                "dataset",
                ObjectType.CONFIG,
                ["cifar10", "imagenet"],
                id="dataset:config",
            ),
            pytest.param("level1", ObjectType.GROUP, ["level2"], id="level1:group"),
            pytest.param("level1", ObjectType.CONFIG, [], id="level1:config"),
            pytest.param(
                "level1/level2",
                ObjectType.CONFIG,
                ["nested1", "nested2"],
                id="level1/level2:config",
            ),
        ],
    )
    def test_config_repository_list(
        self,
        hydra_restore_singletons: Any,
        path: str,
        config_path: str,
        results_filter: Optional[ObjectType],
        expected: List[str],
    ) -> None:
        Plugins.instance()  # initializes
        config_search_path = create_config_search_path(path)
        repo = ConfigRepository(config_search_path=config_search_path)
        ret = repo.get_group_options(
            group_name=config_path, results_filter=results_filter
        )

        assert ret == expected


@pytest.mark.parametrize("sep", [" "])  # type: ignore
@pytest.mark.parametrize(  # type: ignore
    "cfg_text, expected",
    [
        ("# @package{sep}foo.bar", {"package": "foo.bar"}),
        ("# @package{sep} foo.bar", {"package": "foo.bar"}),
        ("# @package {sep}foo.bar", {"package": "foo.bar"}),
        ("#@package{sep}foo.bar", {"package": "foo.bar"}),
        ("#@package{sep}foo.bar ", {"package": "foo.bar"}),
        (
            "#@package{sep}foo.bar bah",
            pytest.raises(ValueError, match=re.escape("Too many components in")),
        ),
        (
            "#@package",
            pytest.raises(
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
