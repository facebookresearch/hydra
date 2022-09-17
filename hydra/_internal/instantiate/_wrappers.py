import copy
from typing import Any, Dict, Optional, Union

from omegaconf.base import Box, DictKeyType, Metadata, Node


# We can't use `omegaconf.nodes.ValueNode` as `omegaconf._utils._get_value` will
# always unpack them
class Boxed(Node):
    def __init__(
        self,
        value: Any = None,
        key: Any = None,
        parent: Optional[Box] = None,
        flags: Optional[Dict[str, bool]] = None,
    ):
        super().__init__(
            parent=parent,
            metadata=Metadata(
                ref_type=Any, object_type=None, key=key, optional=True, flags=flags
            ),
        )
        self._val = value

    def _value(self) -> Any:
        return self._val

    def _set_value(self, value: Any, flags: Optional[Dict[str, bool]] = None) -> None:
        assert flags is None
        self._val = value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Boxed):
            return self._val == other._val
        return False

    def __hash__(self) -> int:
        return self._val.__hash__()

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def _is_interpolation(self) -> bool:
        return False

    def _is_optional(self) -> bool:
        return self._val is None

    def _get_full_key(self, key: Optional[Union[DictKeyType, int]]) -> str:
        parent = self._get_parent()
        if parent is None:
            if self._metadata.key is None:
                return ""
            else:
                return str(self._metadata.key)
        else:
            return parent._get_full_key(self._metadata.key)

    def __repr__(self) -> str:
        return f"Boxed({self._val.__repr__()})"

    def _deepcopy_impl(self, res: Any, memo: Dict[int, Any]) -> None:
        res.__dict__["_metadata"] = copy.deepcopy(self._metadata, memo=memo)
        # shallow copy for value to support non-copyable value
        res.__dict__["_val"] = self._val

        # parent is retained, but not copied
        res.__dict__["_parent"] = self._parent

    def __deepcopy__(self, memo: Dict[int, Any]) -> "Boxed":
        res = Boxed()
        self._deepcopy_impl(res, memo)
        return res
