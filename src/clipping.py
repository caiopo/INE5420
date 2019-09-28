from src.model import Coordinate, Wireframe


class Clipper:
    def __init__(self, vmin: Coordinate, vmax: Coordinate):
        self.vmin = vmin
        self.vmax = vmax

    def clip_point(self, coord: Coordinate):
        if (self.vmin.x <= coord.x <= self.vmax.x
                and self.vmin.y <= coord.y <= self.vmax.y):
            return True, coord
        return False, None

    def clip_line(self, c0: Coordinate, c1: Coordinate):
        return cohen_sutherland(self.vmin, self.vmax, c0, c1)

    def clip_wireframe(self, wireframe: Wireframe):
        pass


CENTER = 0  # 0000
LEFT = 1  # 0001
RIGHT = 2  # 0010
BOTTOM = 4  # 0100
TOP = 8  # 1000


def cohen_sutherland(
        vmin: Coordinate,
        vmax: Coordinate,
        c0: Coordinate,
        c1: Coordinate,
):
    def code(coord: Coordinate):
        _code = CENTER

        if coord.x < vmin.x:
            _code |= LEFT
        elif coord.x > vmax.x:
            _code |= RIGHT

        if coord.y < vmin.y:
            _code |= TOP
        elif coord.y > vmax.y:
            _code |= BOTTOM

        return _code

    while True:
        code0 = code(c0)
        code1 = code(c1)

        if (code0 | code1) == 0:
            return True, c0, c1

        elif (code0 & code1) != 0:
            return False, None, None

        else:
            out = code0 if code0 != 0 else code1

            x = None
            y = None

            if (out & TOP) != 0:
                x = c0.x + (c1.x - c0.x) * (vmin.y - c0.y) / (c1.y - c0.y)
                y = vmin.y

            elif (out & BOTTOM) != 0:
                x = c0.x + (c1.x - c0.x) * (vmax.y - c0.y) / (c1.y - c0.y)
                y = vmax.y

            elif (out & RIGHT) != 0:
                x = vmax.x
                y = c0.y + (c1.y - c0.y) * (vmax.x - c0.x) / (c1.x - c0.x)

            elif (out & LEFT) != 0:
                x = vmin.x
                y = c0.y + (c1.y - c0.y) * (vmin.x - c0.x) / (c1.x - c0.x)

            assert x is not None and y is not None

            if out == code0:
                c0 = Coordinate(x, y)
            else:
                c1 = Coordinate(x, y)
