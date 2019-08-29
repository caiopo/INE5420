from dataclasses import dataclass
from typing import Callable, List

from src.model import Coordinate, Delta, Size, Wireframe

STEP_SIZE = 0.1


@dataclass
class Viewport:
    def __init__(self, size: Size, on_changed: Callable[[], None]):
        self.original_size = size
        self.min = Coordinate(0, 0)
        self.max = Coordinate(size.width, size.height)
        self.current_zoom = 1
        self.on_changed = on_changed

    def reset(self):
        self.__init__(self.original_size, self.on_changed)

    @property
    def size(self):
        return Size(self.max.x - self.min.x, self.max.y - self.min.y)

    def move(self, delta: Delta):
        size_delta = self.size.to_delta() * STEP_SIZE

        self.min += delta * size_delta
        self.max += delta * size_delta
        self._notify()

    def zoom_in(self):
        self.current_zoom += 1
        self.min += self.size.to_delta() / 10
        self.max += self.size.to_delta() / -10
        self._notify()

    def zoom_out(self):
        self.current_zoom -= 1
        self.min += self.size.to_delta() / -10
        self.max += self.size.to_delta() / 10
        self._notify()

    def transform_wireframe(self, wireframe: Wireframe):
        return wireframe.copy(
            coordinates=self.transform_path(wireframe.coordinates)
        )

    def transform_path(self, coordinates: List[Coordinate]):
        return [self.transform_coordinate(c) for c in coordinates]

    def transform_coordinate(self, coordinate: Coordinate) -> Coordinate:
        x = (coordinate.x - self.min.x) / self.size.width * self.original_size.width
        y = (coordinate.y - self.min.y) / self.size.height * self.original_size.height

        return Coordinate(int(x), int(y))

    def untransform_coordinate(self, coordinate: Coordinate) -> Coordinate:
        x = (coordinate.x + self.min.x) / self.size.width * self.original_size.width
        y = (coordinate.y + self.min.y) / self.size.height * self.original_size.height

        return Coordinate(int(x), int(y))

    def _notify(self):
        if self.on_changed is not None:
            self.on_changed()

    def __str__(self):
        return f'Viewport(min={self.min}, max={self.max}, size={self.size}, aspect_ratio={self.size.aspect_ratio})'
