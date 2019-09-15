import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from src.ui.window import WindowHandler
from pathlib import Path

GLADE_FILE = Path(__file__).parent.parent / 'window.glade'


def main():
    builder = Gtk.Builder()
    builder.add_from_file(str(GLADE_FILE))

    window = builder.get_object('main_window')
    builder.connect_signals(WindowHandler(window, builder))

    window.connect('destroy', Gtk.main_quit)

    window.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
