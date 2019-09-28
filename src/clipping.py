from src.model import Coordinate, Wireframe
from src.viewport import Viewport


class Clipper:
    def __init__(self, vp: Viewport):
        self.vp = vp

    def clip_point(self, coord: Coordinate):
        if (self.vp.wmin.x <= coord.x <= self.vp.wmax.x
                and self.vp.wmin.y <= coord.y <= self.vp.wmax.y):
            return coord
        return None

    def clip_line(self, coord1: Coordinate, coord2: Coordinate):
        pass

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

    code0 = code(c0)
    code1 = code(c1)
    accept = False

    while True:
        if (code0 | code1) == 0:
            accept = True
            break

        elif (code0 & code1) != 0:
            break

        else:
            out = code0 if code0 != 0 else code1

        #           // Now find the intersection point;
        # 			// use formulas:
        # 			//   slope = (y1 - y0) / (x1 - x0)
        # 			//   x = x0 + (1 / slope) * (ym - y0), where ym is ymin or ymax
        # 			//   y = y0 + slope * (xm - x0), where xm is xmin or xmax
        # 			// No need to worry about divide-by-zero because, in each case, the
        # 			// outcode bit being tested guarantees the denominator is non-zero
        # 			if (outcodeOut & TOP) {           // point is above the clip window
        # 				x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0);
        # 				y = ymax;
        # 			} else if (outcodeOut & BOTTOM) { // point is below the clip window
        # 				x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0);
        # 				y = ymin;
        # 			} else if (outcodeOut & RIGHT) {  // point is to the right of clip window
        # 				y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0);
        # 				x = xmax;
        # 			} else if (outcodeOut & LEFT) {   // point is to the left of clip window
        # 				y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0);
        # 				x = xmin;
        # 			}

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

        if out == code0:
            c0 = Coordinate(x, y)
