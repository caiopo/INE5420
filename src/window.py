import cairo

from src.display_file import DisplayFile
from src.log import log


class WindowHandler:
    def __init__(self, window, builder):
        self.window = window
        self.builder = builder
        self.df = DisplayFile()
        self.surface = None

    def on_configure_drawing_area(self, drawing_area, event):
        log()

        window = drawing_area.get_window()
        self.surface = window.create_similar_surface(
            cairo.CONTENT_COLOR,
            300,
            200,
        )

        cr = cairo.Context(self.surface)
        cr.set_source_rgb(1, 1, 1)
        cr.paint()

    def on_draw(self, drawing_area, ctx):
        print('on_draw', [drawing_area, ctx])
        ctx.set_source_surface(self.surface, 0, 0)
        ctx.paint()
        return False

    def on_up_pressed(self, *args):
        print('on_up_pressed', args)

    def on_down_pressed(self, *args):
        print('on_down_pressed', args)

    def on_left_pressed(self, *args):
        print('on_left_pressed', args)

    def on_right_pressed(self, *args):
        print('on_right_pressed', args)

    def on_zoom_in_pressed(self, *args):
        print('on_zoom_in_pressed', args)

    def on_zoom_out_pressed(self, *args):
        print('on_zoom_out_pressed', args)
