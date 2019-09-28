from math import pi
from typing import List

import cairo

from src.colors import Color
from src.model import Coordinate, Wireframe


class Pencil:
    def __init__(self, surface):
        self.ctx = cairo.Context(surface)
        self.ctx.set_line_width(1)

    def draw_point(self, point: Coordinate):
        self.ctx.arc(point.x, point.y, 2, 0, 2 * pi)
        self.ctx.fill()
        self.ctx.stroke()

    def draw_path(self, coordinates: List[Coordinate]):
        for i, coord in enumerate(coordinates):
            if i == 0:
                self.ctx.move_to(coord.x, coord.y)
            else:
                self.ctx.line_to(coord.x, coord.y)
        self.ctx.stroke()

    def draw_wireframe(self, wireframe: Wireframe):
        if wireframe.color is not None:
            self.color(wireframe.color)
        else:
            self.ctx.set_source_rgb(0, 0, 0)

        if len(wireframe.coordinates) == 1:
            self.draw_point(wireframe.coordinates[0])
        else:
            self.draw_path(wireframe.coordinates)
        self.ctx.stroke()

    def line_width(self, width):
        self.ctx.set_line_width(width)

    def color(self, color: Color):
        self.ctx.set_source_rgba(*color.to_list())
