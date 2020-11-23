from dataclasses import dataclass
from typing import Optional


@dataclass
class InputDefaultElement:
    # config group name if present
    group: Optional[str] = None
    # config file name
    name: Optional[str] = None
    optional: bool = False
    package: Optional[str] = None


@dataclass
class ProcessedDefaultElement(InputDefaultElement):
    parent: Optional[str] = None

    addressing_key: Optional[str] = None
    result_package: Optional[str] = None
