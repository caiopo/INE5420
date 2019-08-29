from math import pi
from typing import List

import cairo

from src.model import Coordinate, Wireframe


def draw_point(ctx: cairo.Context, point: Coordinate):
    ctx.arc(point.x, point.y, 2, 0, 2 * pi)
    ctx.fill()


def draw_path(ctx: cairo.Context, coordinates: List[Coordinate]):
    for i, coord in enumerate(coordinates):
        if i == 0:
            ctx.move_to(coord.x, coord.y)
        else:
            ctx.line_to(coord.x, coord.y)


def draw_wireframe(ctx: cairo.Context, wireframe: Wireframe):
    if len(wireframe.coordinates) == 1:
        draw_point(ctx, wireframe.coordinates[0])
    else:
        draw_path(ctx, wireframe.coordinates)
        ctx.close_path()
