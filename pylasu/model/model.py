from abc import ABC, abstractmethod
from dataclasses import dataclass, field, InitVar
from typing import Optional, Callable
import ast
import inspect

from .position import Position


class internal_property(property):
    pass


class Origin(ABC):
    @property
    @abstractmethod
    def position(self) -> Position or None:
        pass

    @property
    def source_text(self) -> str or None:
        return None


@dataclass
class JustPosition(Origin):
    position: Position
    _position: Position = field(init=False, repr=False)

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, position: Position):
        self._position = position


def is_internal_property_or_method(value):
    return isinstance(value, internal_property) or isinstance(value, Callable)


@dataclass
class Node(Origin, ast.AST):
    origin: Optional[Origin] = None
    _origin: Origin = field(init=False, repr=False, default=None)
    parent: Optional["Node"] = None
    _parent: "Node" = field(init=False, repr=False, default=None)
    specified_position: InitVar[Position] = None

    def __post_init__(self, specified_position: Position):
        if isinstance(self.origin, property):
            self.origin = None
        if specified_position is not None:
            if self.origin is not None:
                raise Exception("Cannot provide an explicit position when the origin is also specified")
            else:
                self.origin = JustPosition(specified_position)

    @internal_property
    def origin(self) -> Origin:
        return self._origin

    @origin.setter
    def origin(self, origin: Origin):
        self._origin = origin

    @internal_property
    def parent(self) -> "Node":
        return self._parent

    @parent.setter
    def parent(self, parent: "Node"):
        self._parent = parent

    def with_parent(self, parent: "Node"):
        self.parent = parent
        return self

    @internal_property
    def position(self) -> Position:
        return self.origin.position

    @position.setter
    def position(self, position: Position):
        if self.origin is None or isinstance(self.origin, JustPosition):
            self.origin = JustPosition(position)
        else:
            raise Exception("Origin already set, cannot change position")

    @internal_property
    def source_text(self) -> str or None:
        return self.origin.source_text

    @internal_property
    def properties(self):
        return ((name, getattr(self, name)) for name in dir(self)
                if not name.startswith('_')
                and name not in [n for n, v in inspect.getmembers(type(self), is_internal_property_or_method)])

    @internal_property
    def _fields(self):
        yield from (name for name, _ in self.properties)

    @internal_property
    def node_type(self):
        return type(self)
