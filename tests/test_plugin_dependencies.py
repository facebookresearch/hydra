# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import ast
from pathlib import Path
import pytest

PLUGINS_DIR = Path(__file__).parent.parent / "plugins"

EXPECTED_HYDRA_CORE_REQUIREMENT = "hydra-core>=1.4.0.dev1,<1.5.0.dev0"


def get_bundled_plugin_setup_files():
    """Find setup.py for all bundled plugins."""
    setup_files = sorted(PLUGINS_DIR.glob("*/setup.py"))
    assert len(setup_files) > 0, "No bundled plugin setup.py files found"
    return setup_files


@pytest.mark.parametrize("setup_file", get_bundled_plugin_setup_files(), ids=lambda p: p.parent.name)
def test_plugin_hydra_core_dependency_line_versioning(setup_file: Path) -> None:
    """Verify that all bundled plugins specify line-versioning constraints on hydra-core."""
    content = setup_file.read_text(encoding="utf-8")
    tree = ast.parse(content, filename=str(setup_file))

    install_requires_elements = []
    for node in ast.walk(tree):
        if isinstance(node, ast.keyword) and node.arg == "install_requires":
            if isinstance(node.value, ast.List):
                for elt in node.value.elts:
                    if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                        install_requires_elements.append(elt.value)

    hydra_core_deps = [req for req in install_requires_elements if req.startswith("hydra-core")]

    assert len(hydra_core_deps) == 1, (
        f"Expected exactly 1 hydra-core requirement in {setup_file.parent.name}/setup.py, "
        f"found {hydra_core_deps}"
    )

    assert hydra_core_deps[0] == EXPECTED_HYDRA_CORE_REQUIREMENT, (
        f"Plugin {setup_file.parent.name} has incorrect hydra-core dependency '{hydra_core_deps[0]}'. "
        f"Expected '{EXPECTED_HYDRA_CORE_REQUIREMENT}'."
    )
