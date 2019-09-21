from dataclasses import dataclass
from math import pi
from typing import Callable, List

from src.model import Coordinate, Delta, Size, Wireframe
from src.utils import multiples_between

STEP_FACTOR = 10
ROTATION_FACTOR = pi / 8


@dataclass
class Viewport:
    def __init__(self, size: Size, on_changed: Callable[[], None]):
        self.original_size = size
        self.wmin = Coordinate(-size.width / 2, -size.height / 2)
        self.wmax = Coordinate(size.width / 2, size.height / 2)

        self.vmin = Coordinate(0, 0)
        self.vmax = Coordinate(size.width, size.height)

        self.angle = 0

        self.on_changed = on_changed

    def reset(self):
        self.__init__(self.original_size, self.on_changed)

    @property
    def size(self) -> Size:
        return Size(self.wmax.x - self.wmin.x, self.wmax.y - self.wmin.y)

    @property
    def wcenter(self) -> Coordinate:
        return Coordinate(
            (self.wmin.x + self.wmax.x) / 2,
            (self.wmin.y + self.wmax.y) / 2,
        )

    @property
    def vcenter(self) -> Coordinate:
        return Coordinate(
            (self.vmin.x + self.vmax.x) / 2,
            (self.vmin.y + self.vmax.y) / 2,
        )

    def move_to_origin(self):
        self.wmin = Coordinate(-self.original_size.width / 2, -self.original_size.height / 2)
        self.wmax = Coordinate(self.original_size.width / 2, self.original_size.height / 2)
        self.angle = 0
        self._notify()

    def move(self, delta: Delta):
        size_delta = self.size.to_delta() / STEP_FACTOR

        self.wmin += delta * size_delta
        self.wmax += delta * size_delta
        self._notify()

    def zoom_in(self):
        self.wmin += self.size.to_delta() / 10
        self.wmax += self.size.to_delta() / -10
        self._notify()

    def zoom_out(self):
        self.wmin += self.size.to_delta() / -10
        self.wmax += self.size.to_delta() / 10
        self._notify()

    def rotate_clockwise(self):
        self.angle += ROTATION_FACTOR
        self._notify()

    def rotate_counterclockwise(self):
        self.angle -= ROTATION_FACTOR
        self._notify()

    def transform_wireframes(self, wireframes: List[Wireframe]):
        return [
            w.copy(coordinates=self.transform_path(w.coordinates))
            for w in wireframes
        ]

    def transform_wireframe(self, wireframe: Wireframe) -> Wireframe:
        return wireframe.copy(
            coordinates=self.transform_path(wireframe.coordinates)
        )

    def transform_path(self, coordinates: List[Coordinate]):
        return [self.transform_coordinate(c) for c in coordinates]

    def transform_coordinate(self, coordinate: Coordinate) -> Coordinate:
        coordinate = coordinate.rotate(self.wcenter, self.angle)

        x = (coordinate.x - self.wmin.x) / (self.wmax.x - self.wmin.x) * (self.vmax.x - self.vmin.x)
        y = (coordinate.y - self.wmin.y) / (self.wmax.y - self.wmin.y) * (self.vmax.y - self.vmin.y)

        return Coordinate(x, y)

    def untransform_coordinate(self, coordinate: Coordinate) -> Coordinate:
        coordinate = coordinate.rotate(self.vcenter, -self.angle)

        x = coordinate.x / (self.vmax.x - self.vmin.x) * (self.wmax.x - self.wmin.x) + self.wmin.x
        y = coordinate.y / (self.vmax.y - self.vmin.y) * (self.wmax.y - self.wmin.y) + self.wmin.y

        return Coordinate(x, y)

    def get_grid(self):
        size = self.size

        lines = [
            Wireframe.line('red', (self.wmin.x - size.width, y), (self.wmax.x + size.width, y))
            for y in multiples_between(self.wmin.y - size.height, self.wmax.y + size.height, 100)
        ]

        columns = [
            Wireframe.line('blue', (x, self.wmin.y - size.height), (x, self.wmax.y + size.height))
            for x in multiples_between(self.wmin.x - size.width, self.wmax.x + size.width, 100)
        ]

        return self.transform_wireframes(lines + columns)

    def _notify(self):
        if self.on_changed is not None:
            self.on_changed()

    def __str__(self):
        return (f'Viewport(wmin={self.wmin}, wmax={self.wmax}, angle={self.angle}, '
                f'size={self.size}, aspect_ratio={self.size.aspect_ratio}), wcenter={self.wcenter}')
