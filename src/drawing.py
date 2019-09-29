from math import pi

import cairo

from src.colors import Color
from src.model import Coordinate, Wireframe


class Pencil:
    def __init__(self, surface, vmin: Coordinate, vmax: Coordinate):
        self.ctx = cairo.Context(surface)
        self.ctx.set_line_width(1)

        self.vmin = vmin
        self.vmax = vmax

    def draw_point(self, point: Coordinate):
        self.ctx.arc(point.x, point.y, 2, 0, 2 * pi)
        self.ctx.fill()
        self.ctx.stroke()

    def draw_wireframe(self, wireframe: Wireframe):
        if wireframe.color is not None:
            self.color(wireframe.color)
        else:
            self.ctx.set_source_rgb(0, 0, 0)

        if len(wireframe.coordinates) == 1:
            self.draw_point(wireframe.coordinates[0])
        else:
            for line in wireframe.lines:
                self._draw_line(*line)

    def line_width(self, width):
        self.ctx.set_line_width(width)

    def color(self, color: Color):
        self.ctx.set_source_rgba(*color.to_list())

    def _draw_line(self, c0: Coordinate, c1: Coordinate):
        self.ctx.move_to(c0.x, c0.y)
        self.ctx.line_to(c1.x, c1.y)
        self.ctx.stroke()

        # clipper = Clipper(self.vmin, self.vmax)
        #
        # inside, c0, c1 = clipper.cohen_sutherland(c0, c1)
        #
        # if inside:
        #     self.ctx.move_to(c0.x, c0.y)
        #     self.ctx.line_to(c1.x, c1.y)
        #     self.ctx.stroke()
