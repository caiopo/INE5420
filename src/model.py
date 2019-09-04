from dataclasses import dataclass, field, replace
from typing import List


@dataclass
class Coordinate:
    x: float
    y: float

    def __post_init__(self):
        self.x = float(self.x)
        self.y = float(self.y)

    def __add__(self, other):
        assert isinstance(other, Delta)
        return Coordinate(
            self.x + other.x,
            self.y + other.y,
        )

    def __mul__(self, other):
        if isinstance(other, Delta):
            return Coordinate(
                self.x * other.x,
                self.y * other.y
            )
        return Coordinate(
            self.x * other,
            self.y * other
        )

    def __str__(self):
        return str((self.x, self.y))


@dataclass
class Wireframe:
    id: str
    coordinates: List[Coordinate] = field(default_factory=list)

    def copy(self, **changes):
        return replace(self, **changes)


@dataclass
class Size:
    width: int
    height: int

    @property
    def aspect_ratio(self):
        return self.width / self.height

    def to_delta(self):
        return Delta(
            self.width,
            self.height,
        )


@dataclass
class Delta:
    x: float
    y: float

    def __add__(self, other):
        assert isinstance(other, Delta)
        return Delta(
            self.x + other.x,
            self.y + other.y,
        )

    def __mul__(self, other):
        if isinstance(other, Delta):
            return Delta(
                self.x * other.x,
                self.y * other.y,
            )
        return Delta(
            self.x * other,
            self.y * other,
        )

    def __truediv__(self, other):
        return self * (1 / other)


class Direction:
    UP = Delta(0, -1)
    DOWN = Delta(0, 1)
    LEFT = Delta(-1, 0)
    RIGHT = Delta(1, 0)
