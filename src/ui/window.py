from typing import Optional

import cairo

from src.display_file import DisplayFile
from src.drawing import draw_path, draw_point, draw_wireframe
from src.log import log
from src.model import Coordinate, Direction, Size
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
            result.apply(self.df)
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

        ctx = cairo.Context(self.surface)

        ctx.set_line_width(1)

        for wireframe in self.vp.get_grid():
            if wireframe.id == 'blue':
                ctx.set_source_rgba(0, 0, 1, 0.3)
            else:
                ctx.set_source_rgba(1, 0, 0, 0.3)

            draw_wireframe(ctx, wireframe)
            ctx.stroke()

        ctx.set_source_rgba(0, 0, 0, 0.5)
        ctx.set_line_width(10)

        origin = self.vp.transform_coordinate(Coordinate(0, 0))
        draw_point(ctx, origin)
        ctx.stroke()

        ctx.set_line_width(1.5)
        ctx.set_source_rgb(0, 0, 0)

        for wireframe in self.df.wireframes:
            transformed_wireframe = self.vp.transform_wireframe(wireframe)
            draw_wireframe(ctx, transformed_wireframe)
            ctx.stroke()

        if self.creating_wireframe is not None:
            ctx.set_source_rgb(1, 0, 0)
            transformed_path = self.vp.transform_path(self.creating_wireframe)
            if len(transformed_path) == 1:
                draw_point(ctx, transformed_path[0])
            else:
                draw_path(ctx, transformed_path)

            ctx.stroke()

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