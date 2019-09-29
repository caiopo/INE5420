from typing import Optional

import cairo

from src.clipping import Clipper
from src.colors import Color
from src.display_file import DisplayFile
from src.drawing import Pencil
from src.log import log
from src.model import Coordinate, Direction, Size, Wireframe
from src.ui.transform_dialog import TransformDialogHandler, TransformResult
from src.viewport import Viewport


class WindowHandler:
    def __init__(self, window, builder):
        self.window = window
        self.builder = builder
        self.df = DisplayFile()
        self.vp: Optional[Viewport] = None
        self.surface = None
        self.creating_wireframe = None

    def on_configure_drawing_area(self, drawing_area, event):
        log(event)

        window = drawing_area.get_window()
        width = drawing_area.get_allocated_width()
        height = drawing_area.get_allocated_height()

        self.vp = Viewport(size=Size(width, height), on_changed=self._refresh)

        self.surface = window.create_similar_surface(
            cairo.CONTENT_COLOR,
            width,
            height,
        )
        self._refresh()
        return True

    def on_press_drawing_area(self, drawing_area, event):
        click = Coordinate(event.x, event.y)

        if self.creating_wireframe is not None:
            untransformed_click = self.vp.untransform_coordinate(click)
            self.creating_wireframe.append(untransformed_click)
            self._refresh()

        return True

    def on_draw(self, drawing_area, ctx):
        ctx.set_source_surface(self.surface, 0, 0)
        ctx.paint()
        return False

    def on_add_toggle(self, toggle_button):
        active = toggle_button.get_active()

        if active:
            self.creating_wireframe = []
        else:
            if len(self.creating_wireframe) > 2:
                self.creating_wireframe.append(self.creating_wireframe[0])

            self.df.add(self.creating_wireframe)
            self.creating_wireframe = None
        self._refresh()

    def on_move_to_origin_pressed(self, *args):
        log(args)
        self.vp.move_to_origin()

    def on_transform_pressed(self, *args):
        log(args)
        TransformDialogHandler(self.on_transform_completed)

    def on_transform_completed(self, result: TransformResult):
        log(result)

        if result is None:
            return

        try:
            result.apply(self.df, self.vp)
        except ValueError as e:
            print('transform error:', e)

        self._refresh()

    def on_reset_pressed(self, *args):
        log(args)
        self.builder.get_object('add_wireframe_button').set_active(False)
        self.df.reset()
        self.vp.reset()
        self._refresh()

    def on_drag_begin(self, *args):
        log(args)

    def on_drag_end(self, *args):
        log(args)

    def on_up_pressed(self, *args):
        self.vp.move(Direction.UP)
        log(self.vp)

    def on_down_pressed(self, *args):
        self.vp.move(Direction.DOWN)
        log(self.vp)

    def on_left_pressed(self, *args):
        self.vp.move(Direction.LEFT)
        log(self.vp)

    def on_right_pressed(self, *args):
        self.vp.move(Direction.RIGHT)
        log(self.vp)

    def on_zoom_in_pressed(self, *args):
        self.vp.zoom_in()
        log(self.vp)

    def on_zoom_out_pressed(self, *args):
        self.vp.zoom_out()
        log(self.vp)

    def on_rotate_clockwise_pressed(self, *args):
        self.vp.rotate_clockwise()
        log(self.vp)

    def on_rotate_counterclockwise_pressed(self, *args):
        self.vp.rotate_counterclockwise()
        log(self.vp)

    def _clear_surface(self):
        ctx = cairo.Context(self.surface)
        ctx.set_source_rgb(1, 1, 1)
        ctx.paint()

    def _refresh(self):
        self._refresh_list()
        self._clear_surface()

        pencil = Pencil(self.surface, self.vp.vmin, self.vp.vmax)
        clipper = Clipper(self.vp.vmin, self.vp.vmax)

        for wireframe in self.vp.get_grid():
            clipped_wireframes = clipper.clip(wireframe)
            for w in clipped_wireframes:
                pencil.draw_wireframe(w)

        pencil.line_width(10)
        pencil.color(Color(0, 0, 0, 0.5))

        origin = self.vp.transform_coordinate(Coordinate(0, 0))
        pencil.draw_point(origin)

        pencil.line_width(1.5)

        for wireframe in self.df.wireframes:
            transformed_wireframe = self.vp.transform_wireframe(wireframe)

            clipped_wireframe = clipper.clip(transformed_wireframe)

            for w in clipped_wireframe:
                pencil.draw_wireframe(w)

        if self.creating_wireframe is not None:
            new_wireframe = Wireframe(
                id='creating',
                coordinates=self.creating_wireframe,
                color=Color(1, 0, 0)
            )

            transformed_wireframe = self.vp.transform_wireframe(new_wireframe)
            pencil.draw_wireframe(transformed_wireframe)

        clipping_square = Wireframe.square(
            'clipping_square',
            self.vp.vmin,
            self.vp.vmax,
            color=Color(1, 0.5, 0),
        )

        pencil.draw_wireframe(clipping_square)

        self.window.queue_draw()

    def _refresh_list(self):
        wireframe_list = ['Objects:']

        if len(self.df.wireframes) == 0:
            wireframe_list = ['No objects', 'added yet']

        for wireframe in self.df.wireframes:
            t = 'Polygon'

            coord_len = len(wireframe.coordinates)
            if coord_len == 1:
                t = 'Point'
            elif coord_len == 2:
                t = 'Line'

            wireframe_list.extend([
                '',
                f'ID: {wireframe.id}',
                f'Type: {t}',
            ])

            for i, c in enumerate(wireframe.coordinates):
                wireframe_list.append(f'C{i}: ({round(c.x)}, {round(c.y)})')

            center = wireframe.center
            wireframe_list.append(f'Center: ({round(center.x)}, {round(center.y)})')

        wireframe_list.append('')

        self.builder.get_object('wireframe_list').set_text('\n'.join(wireframe_list))
