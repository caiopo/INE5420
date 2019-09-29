from dataclasses import dataclass, field, replace
from math import cos, sin
from typing import List, Tuple

import numpy as np

from src.colors import Color


class Coordinate:
    @staticmethod
    def from_array(v: np.array):
        return Coordinate(v[0], v[1])

    def __init__(self, x: float, y: float, w: float = 1):
        self.v = np.array([x, y, w], dtype=float)

    @property
    def x(self):
        return self.v[0]

    @property
    def y(self):
        return self.v[1]

    def rotate(self, anchor: 'Coordinate', theta: float):
        t_origin = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [-anchor.x, -anchor.y, 1],
        ])

        rotate = np.array([
            [cos(theta), -sin(theta), 0],
            [sin(theta), cos(theta), 0],
            [0, 0, 1],
        ])

        t_back = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [anchor.x, anchor.y, 1],
        ])

        return self @ t_origin @ rotate @ t_back

    def __add__(self, other):
        if isinstance(other, Delta):
            return Coordinate.from_array(self.v + other.v)

        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Delta):
            return Coordinate.from_array(self.v * other.v)

        if isinstance(other, (int, float)):
            return Coordinate.from_array(self.v * other)

    def __matmul__(self, other):
        if isinstance(other, np.ndarray):
            return Coordinate.from_array(self.v @ other)

        return NotImplemented

    def __eq__(self, other):
        e = isinstance(other, Coordinate) and (self.v == other.v).all()
        # print(self, other, e)
        return e

    def __str__(self):
        return str((self.x, self.y))

    def __repr__(self):
        return str(self)


@dataclass
class Wireframe:
    id: str
    coordinates: List[Coordinate] = field(default_factory=list)
    color: Color = None

    def copy(self, **changes):
        return replace(self, **changes)

    @staticmethod
    def line(oid, xy1, xy2, color=None):
        x1, y1 = xy1
        x2, y2 = xy2
        return Wireframe(
            oid,
            coordinates=[
                Coordinate(x1, y1),
                Coordinate(x2, y2),
            ],
            color=color,
        )

    @staticmethod
    def point(oid, x, y, color=None):
        return Wireframe(
            oid,
            coordinates=[
                Coordinate(x, y),
            ],
            color=color,
        )

    @staticmethod
    def square(oid, xy1, xy2, color=None):
        x1, y1 = _unpack(xy1)
        x2, y2 = _unpack(xy2)

        minx = min(x1, x2)
        maxx = max(x1, x2)

        miny = min(y1, y2)
        maxy = max(y1, y2)

        return Wireframe(
            oid,
            coordinates=[
                Coordinate(minx, miny),
                Coordinate(maxx, miny),
                Coordinate(maxx, maxy),
                Coordinate(minx, maxy),
                Coordinate(minx, miny),
            ],
            color=color,
        )

    @property
    def center(self) -> Coordinate:
        cx = 0
        cy = 0

        for c in self.coordinates:
            cx += c.x
            cy += c.y

        cx /= len(self.coordinates)
        cy /= len(self.coordinates)

        return Coordinate(cx, cy)

    @property
    def lines(self) -> List[Tuple[Coordinate, Coordinate]]:
        return list(zip(self.coordinates, self.coordinates[1:]))

    def _apply_transformation(self, t):
        return self.copy(coordinates=[c @ t for c in self.coordinates])

    def translate(self, delta: 'Delta'):
        t = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [delta.x, delta.y, 1],
        ])

        return self._apply_transformation(t)

    def scale(self, delta: 'Delta'):
        center = self.center

        t_origin = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [-center.x, -center.y, 1],
        ])

        scale = np.array([
            [delta.x, 0, 0],
            [0, delta.y, 0],
            [0, 0, 1],
        ])

        t_back = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [center.x, center.y, 1],
        ])

        return self._apply_transformation(t_origin @ scale @ t_back)

    def rotate_on_world(self, theta: float):
        return self.rotate_on_coordinate(Coordinate(0, 0), theta)

    def rotate_on_center(self, theta: float):
        return self.rotate_on_coordinate(self.center, theta)

    def rotate_on_coordinate(self, coordinate: Coordinate, theta: float):
        t_origin = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [-coordinate.x, -coordinate.y, 1],
        ])

        rotate = np.array([
            [cos(theta), -sin(theta), 0],
            [sin(theta), cos(theta), 0],
            [0, 0, 1],
        ])

        t_back = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [coordinate.x, coordinate.y, 1],
        ])

        return self._apply_transformation(t_origin @ rotate @ t_back)


@dataclass
class Size:
    width: float
    height: float

    @property
    def aspect_ratio(self):
        return self.width / self.height

    def to_delta(self):
        return Delta(
            self.width,
            self.height,
        )


class Delta:
    @staticmethod
    def from_array(arr: np.array):
        return Delta(arr[0], arr[1])

    def __init__(self, x: float, y: float):
        self.v = np.array([x, y, 0], dtype=float)

    def rotate(self, theta: float):
        rotate = np.array([
            [cos(theta), -sin(theta), 0],
            [sin(theta), cos(theta), 0],
            [0, 0, 1],
        ])

        return Delta.from_array(self.v @ rotate)

    @property
    def x(self):
        return self.v[0]

    @x.setter
    def x(self, value):
        self.v[0] = value

    @property
    def y(self):
        return self.v[1]

    @y.setter
    def y(self, value):
        self.v[1] = value

    def __add__(self, other):
        if isinstance(other, Delta):
            return Delta.from_array(self.v + other.v)

        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Delta):
            return Delta.from_array(self.v * other.v)

        if isinstance(other, (int, float)):
            return Delta.from_array(self.v * other)

        return NotImplemented

    def __truediv__(self, other):
        return self * (1 / other)

    def __str__(self):
        return str((self.x, self.y))


class Direction:
    UP = Delta(0, -1)
    DOWN = Delta(0, 1)
    LEFT = Delta(-1, 0)
    RIGHT = Delta(1, 0)


def _unpack(xy):
    if isinstance(xy, Coordinate):
        return xy.x, xy.y
    return xy
