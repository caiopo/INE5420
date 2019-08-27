import gi

from src.window import WindowHandler

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def main():
    builder = Gtk.Builder()
    builder.add_from_file('../window.glade')

    window = builder.get_object('main_window')
    builder.connect_signals(WindowHandler(window, builder))

    window.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
