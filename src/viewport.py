from dataclasses import dataclass
from typing import Callable, List

from src.model import Coordinate, Delta, Size, Wireframe

STEP_SIZE = 0.1


@dataclass
class Viewport:
    def __init__(self, size: Size, on_changed: Callable[[], None]):
        self.original_size = size
        self.wmin = Coordinate(0, 0)
        self.wmax = Coordinate(size.width, size.height)

        self.vmin = Coordinate(0, 0)
        self.vmax = Coordinate(size.width, size.height)

        self.current_zoom = 1
        self.on_changed = on_changed

    def reset(self):
        self.__init__(self.original_size, self.on_changed)

    @property
    def size(self):
        return Size(self.wmax.x - self.wmin.x, self.wmax.y - self.wmin.y)

    def move(self, delta: Delta):
        size_delta = self.size.to_delta() * STEP_SIZE

        self.wmin += delta * size_delta
        self.wmax += delta * size_delta
        self._notify()

    def zoom_in(self):
        self.current_zoom += 1
        self.wmin += self.size.to_delta() / 10
        self.wmax += self.size.to_delta() / -10
        self._notify()

    def zoom_out(self):
        self.current_zoom -= 1
        self.wmin += self.size.to_delta() / -10
        self.wmax += self.size.to_delta() / 10
        self._notify()

    def transform_wireframe(self, wireframe: Wireframe):
        return wireframe.copy(
            coordinates=self.transform_path(wireframe.coordinates)
        )

    def transform_path(self, coordinates: List[Coordinate]):
        return [self.transform_coordinate(c) for c in coordinates]

    def transform_coordinate(self, coordinate: Coordinate) -> Coordinate:
        x = (coordinate.x - self.wmin.x) / (self.wmax.x - self.wmin.x) * (self.vmax.x - self.vmin.x)
        y = (coordinate.y - self.wmin.y) / (self.wmax.y - self.wmin.y) * (self.vmax.y - self.vmin.y)

        return Coordinate(x, y)

    def untransform_coordinate(self, coordinate: Coordinate) -> Coordinate:
        x = coordinate.x / (self.vmax.x - self.vmin.x) * (self.wmax.x - self.wmin.x) + self.wmin.x
        y = coordinate.y / (self.vmax.y - self.vmin.y) * (self.wmax.y - self.wmin.y) + self.wmin.y

        return Coordinate(x, y)

    def _notify(self):
        if self.on_changed is not None:
            self.on_changed()

    def __str__(self):
        return f'Viewport(wmin={self.wmin}, wmax={self.wmax}, size={self.size}, aspect_ratio={self.size.aspect_ratio})'
