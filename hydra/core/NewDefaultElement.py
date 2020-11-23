from dataclasses import dataclass
from typing import Optional


@dataclass
class InputDefault:
    # config group name if present
    group: Optional[str] = None
    # config file name
    name: Optional[str] = None
    optional: bool = False
    package: Optional[str] = None

    def is_self(self) -> bool:
        return self.name == "_self_"
