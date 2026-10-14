# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""Compare default instantiation with experimental isolate=True.

Run from the repository root:
    PYTHONPATH=. .venv/bin/python temp/repro/3537.py
"""

import pickle
from dataclasses import dataclass, field

from omegaconf import OmegaConf

from hydra.utils import instantiate


class Model:
    def __init__(self, sizes):
        self.sizes = sizes


def make_config():
    @dataclass
    class ModelConf:
        _target_: str = "__main__.Model"
        sizes: list = field(default_factory=lambda: [1, 2, 3])

    return ModelConf


@dataclass
class ModelConf:
    _target_: str = "__main__.Model"
    sizes: list = field(default_factory=lambda: [1, 2, 3])


@dataclass
class Experiment:
    model: ModelConf = field(default_factory=ModelConf)
    data: list = field(default_factory=lambda: list(range(100_000)))


def main():
    for isolate in (False, True):
        print(f"\nisolate={isolate}")
        model = instantiate(
            make_config(), isolate=isolate, _execution_whitelist_="__main__.Model"
        )
        print("sizes type:", type(model.sizes).__name__)
        print("sizes has parent:", model.sizes._get_parent() is not None)
        try:
            print("local-schema model pickle bytes:", len(pickle.dumps(model)))
        except (pickle.PicklingError, AttributeError) as exc:
            print("local-schema model pickle:", type(exc).__name__, str(exc))

        cfg = OmegaConf.create(
            {
                "width": 8,
                "model": {
                    "_target_": "__main__.Model",
                    "_recursive_": False,
                    "sizes": ["${width}", 16],
                },
            }
        )
        interpolated = instantiate(
            cfg.model, isolate=isolate, _execution_whitelist_="__main__.Model"
        )
        print("raw sizes:", OmegaConf.to_container(interpolated.sizes, resolve=False))
        cfg.width = 32
        print("sizes after source width changes:", list(interpolated.sizes))

        experiment = instantiate(
            Experiment, isolate=isolate, _execution_whitelist_="__main__.Model"
        )
        print(
            "three-item sizes pickle bytes:", len(pickle.dumps(experiment.model.sizes))
        )

    @dataclass
    class IsolatedModelConf(make_config()):
        _isolate_: bool = True

    print("\nGenerated config with _isolate_=True")
    for explicit in ("omitted", False, True):
        options = {} if explicit == "omitted" else {"isolate": explicit}
        model = instantiate(
            IsolatedModelConf, _execution_whitelist_="__main__.Model", **options
        )
        print(
            f"isolate={explicit}: sizes has parent:",
            model.sizes._get_parent() is not None,
        )
        if explicit:
            print("model pickle bytes:", len(pickle.dumps(model)))


if __name__ == "__main__":
    main()
