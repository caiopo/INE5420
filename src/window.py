from math import pi

import cairo

from src.display_file import DisplayFile
from src.log import log
from src.model import Coordinate, Polygon


class WindowHandler:
    def __init__(self, window, builder):
        self.window = window
        self.builder = builder
        self.df = DisplayFile()
        self.surface = None

    def on_configure_drawing_area(self, drawing_area, event):
        log()

        window = drawing_area.get_window()
        width = drawing_area.get_allocated_width()
        height = drawing_area.get_allocated_height()

        self.surface = window.create_similar_surface(
            cairo.CONTENT_COLOR,
            width,
            height,
        )
        self._refresh()
        return True

    def on_click_drawing_area(self, drawing_area, event):
        click = Coordinate(event.x, event.y)
        log(click)

    def on_draw(self, drawing_area, ctx):
        ctx.set_source_surface(self.surface, 0, 0)
        ctx.paint()
        return False

    def on_up_pressed(self, *args):
        log(args)

    def on_down_pressed(self, *args):
        log(args)

    def on_left_pressed(self, *args):
        log(args)

    def on_right_pressed(self, *args):
        log(args)

    def on_zoom_in_pressed(self, *args):
        log(args)
        self._refresh()

    def on_zoom_out_pressed(self, *args):
        log(args)

    def _clear_surface(self):
        cr = cairo.Context(self.surface)
        cr.set_source_rgb(1, 1, 1)
        cr.paint()

    def _refresh(self):
        self._clear_surface()

        ctx = cairo.Context(self.surface)
        ctx.set_source_rgb(0, 0, 0)

        for obj in self.df:
            self._draw_obj(ctx, obj)

        ctx.stroke()
        self.window.queue_draw()

    def _draw_obj(self, ctx: cairo.Context, obj: Polygon):
        if obj.is_point:
            ctx.arc(obj.first.x, obj.first.y, 2, 0, 2 * pi)
            ctx.fill_preserve()

        else:
            for i, coord in enumerate(obj.coordinates):
                if i == 0:
                    ctx.move_to(coord.x, coord.y)
                else:
                    ctx.line_to(coord.x, coord.y)
