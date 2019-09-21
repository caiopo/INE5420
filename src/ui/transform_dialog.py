from dataclasses import dataclass
from pathlib import Path

from gi.overrides import Gtk

from src.display_file import DisplayFile
from src.log import log
from src.model import Coordinate, Delta
from src.utils import try_float
from src.viewport import Viewport

GLADE_FILE = Path(__file__).parent.parent.parent / 'transform_dialog.glade'


@dataclass
class TransformResult:
    oid: str
    type: str
    x: float
    y: float
    theta: float

    def apply(self, df: DisplayFile, vp: Viewport):
        wireframe = df[self.oid]

        if wireframe is None:
            raise ValueError('invalid oid')

        new = None

        if self.type == 'translate':
            if self.x is None or self.y is None:
                raise ValueError('scale')

            new = wireframe.translate(Delta(self.x, self.y).rotate(-vp.angle))

        if self.type == 'scale':
            if self.x is None or self.y is None:
                raise ValueError('scale')

            new = wireframe.scale(Delta(self.x, self.y))

        if self.type == 'rotate_world':
            if self.theta is None:
                raise ValueError('rotate_world')

            new = wireframe.rotate_on_world(self.theta)

        if self.type == 'rotate_coordinate':
            if self.x is None or self.y is None or self.theta is None:
                raise ValueError('rotate_coordinate')

            new = wireframe.rotate_on_coordinate(Coordinate(self.x, self.y), self.theta)

        if self.type == 'rotate_self':
            if self.theta is None:
                raise ValueError('rotate_self')

            new = wireframe.rotate_on_center(self.theta)

        if new is not None:
            df.replace(self.oid, new)


class TransformDialogHandler:
    def __init__(self, on_complete):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(str(GLADE_FILE))
        self.builder.connect_signals(self)

        self.on_complete = on_complete

        self.dialog = self.builder.get_object('transform_dialog')

        self.input_oid = self.builder.get_object('input_oid')
        self.input_x = self.builder.get_object('input_x')
        self.input_y = self.builder.get_object('input_y')
        self.input_theta = self.builder.get_object('input_theta')

        # self.input_oid.set_text('')
        # self.input_x.set_text('')
        # self.input_y.set_text('')
        # self.input_theta.set_text('')

        self.radios = [
            (wid, self.builder.get_object(wid))
            for wid in ['translate', 'scale', 'rotate_world', 'rotate_coordinate', 'rotate_self']
        ]

        for wid, radio in self.radios:
            radio.connect('toggled', self.on_radio_toggled, wid)

        self._selected_type = 'translate'

        # self.builder.get_object('done_button').connect('clicked', self.on_done_pressed)
        # self.builder.get_object('cancel_button').connect('clicked', self.on_cancel_pressed)

        self.dialog.show_all()

    def on_done_pressed(self, *args):
        oid = self.input_oid.get_text()
        x = self.input_x.get_text()
        y = self.input_y.get_text()
        theta = self.input_theta.get_text()

        self.dialog.hide()

        result = TransformResult(
            oid=oid,
            type=self._selected_type,
            x=try_float(x),
            y=try_float(y),
            theta=try_float(theta),
        )

        self.on_complete(result)

    def on_cancel_pressed(self, *args):
        self.dialog.hide()
        self.on_complete(None)

    def on_radio_toggled(self, radio, wid):
        if radio.get_active():
            log(wid)
            self._selected_type = wid
