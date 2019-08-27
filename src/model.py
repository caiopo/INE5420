from dataclasses import dataclass, field
from enum import Enum
from typing import List


@dataclass
class Coordinate:
    x: int
    y: int

    def __add__(self, other):
        assert isinstance(other, Delta)
        return Coordinate(
            self.x + other.x,
            self.y + other.y,
        )


@dataclass
class Polygon:
    id: str
    coordinates: List[Coordinate] = field(default_factory=list)

    @property
    def is_point(self):
        return len(self.coordinates) == 1

    @property
    def first(self):
        return self.coordinates[0]


@dataclass
class Size:
    width: int
    height: int


@dataclass
class Delta:
    x: int
    y: int

    def __mul__(self, other):
        return Delta(
            self.x * other,
            self.y * other,
        )


class Direction(Enum):
    UP = Delta(-1, 0)
    DOWN = Delta(1, 0)
    LEFT = Delta(0, -1)
    RIGHT = Delta(0, 1)
