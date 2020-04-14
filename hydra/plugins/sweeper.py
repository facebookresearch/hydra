# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Sweeper plugin interface
"""
import itertools
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

from omegaconf import DictConfig

from hydra.core.config_loader import ConfigLoader
from hydra.types import TaskFunction

from .plugin import Plugin


class Sweeper(Plugin):
    """
    An abstract sweeper interface
    Sweeper takes the command line arguments, generates a and launches jobs
    (where each job typically takes a different command line arguments)
    """

    @abstractmethod
    def setup(
        self,
        config: DictConfig,
        config_loader: ConfigLoader,
        task_function: TaskFunction,
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def sweep(self, arguments: List[str]) -> Any:
        """
        Execute a sweep
        :param arguments: list of strings describing what this sweeper should do.
        exact structure is determine by the concrete Sweeper class.
        :return: the return objects of all thy launched jobs. structure depends on the Sweeper
        implementation.
        """
        ...


@dataclass
class CommandlineSpec:
    """Structured commandline specification
    for sweepers handling categorical variables and bounded variables

    Attributes
    ----------
    bounds: Optional[Tuple[float, float]]
        if present, this defines a bounded scalar between bounds[0]
        and bounds[1]
    options: Optional[List[Any]]
        if present, this defines the options/choices of a categorical
        variable
    cast: str
        the name of the variable type to cast it to ("int", "str"
        or "float")
    log: bool
        for bounded scalars, whether it is log-distributed

    Note
    ----
    Exactly one of bounds or options must be provided
    """

    bounds: Optional[Tuple[float, float]] = None
    options: Optional[List[str]] = None
    cast: str = "float"
    log: bool = False

    def __post_init__(self) -> None:
        if not (self.bounds is None) ^ (self.options is None):
            raise ValueError("Exactly one of bounds or options must be specified")
        if self.bounds is not None:
            if self.cast == "str":
                raise ValueError(
                    "Inconsistent specifications 'str' for bounded values."
                )
            if self.bounds[0] > self.bounds[1]:
                raise ValueError(f"Bounds must be ordered, but got {self.bounds}")
        if self.options is not None and self.log:
            raise ValueError("Inconsistent 'log' specification for choice parameter")

    @classmethod
    def parse(cls, string: str) -> "CommandlineSpec":
        """Parses a commandline argument string

        Parameter
        ---------
        string: str
            This can be:
             - comma-separated values: for a choice parameter
               Eg.: "a,b,c"
             - colon-separated values for ranges of scalars.
               Eg.: "0:10"
            Colon-separeted can be appended to:
             - cast to int/str/float (always defaults to float):
               Eg: "float:0,4,10", "int:0:10"
             - set log distribution for scalars
               Eg: "int:log:4:1024"
        """
        available_modifiers = {"log", "float", "int", "str"}
        colon_split = string.split(":")
        modifiers = set(
            itertools.takewhile(available_modifiers.__contains__, colon_split)
        )
        remain = colon_split[len(modifiers) :]
        casts = list(modifiers - {"log"})
        if len(remain) not in {1, 2}:
            raise ValueError(
                "Can't interpret non-speficiations: {}.\nthis needs to be "
                "either colon or coma-separated values".format(":".join(remain))
            )
        if len(casts) > 1:
            raise ValueError(f"Inconsistent specifications: {casts}")
        if len(remain) == 1:  # choice argument
            cast = casts[0] if casts else "str"
            options = remain[0].split(",")
            if len(options) < 2:
                raise ValueError("At least 2 options are required")
            if not casts:
                try:  # default to float if possible and no spec provided
                    _ = [float(x) for x in options]
                    cast = "float"
                except ValueError:
                    pass
            return cls(options=options, cast=cast)
        # bounded argument
        bounds: Tuple[float, float] = tuple(float(x) for x in remain)  # type: ignore
        cast = casts[0] if casts else "float"
        return cls(bounds=bounds, cast=cast, log="log" in modifiers)
