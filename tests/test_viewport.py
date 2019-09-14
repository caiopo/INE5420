from src.model import Coordinate, Delta, Size
from src.viewport import Viewport
from tests.util import almost_equal


def test_viewport_transform():
    vp = Viewport(Size(80, 60))
    vp.move(Delta(10, 5))
    vp.zoom_in()
    vp.zoom_in()

    c = Coordinate(100, 50)

    tc = vp.transform_coordinate(c)
    assert tc == Coordinate(60, 50)

    uc = vp.untransform_coordinate(tc)
    assert c == uc


def test_viewport_move():
    vp = Viewport(Size(80, 60))
    vp.move(Delta(10, 5))

    assert almost_equal(vp.wmin, Coordinate(40, 0))
    assert vp.wmax == Coordinate(120, 60)


def test_viewport_zoom():
    vp = Viewport(Size(80, 60))
    original_wmin = vp.wmin
    original_wmax = vp.wmax

    vp.zoom_out()
    vp.zoom_out()

    assert almost_equal(vp.wmin, Coordinate(-57.68, -43.26))
    assert almost_equal(vp.wmax, Coordinate(59.4, 44.586))

    vp.zoom_in()
    vp.zoom_in()

    assert vp.wmin == original_wmin
    assert vp.wmax == original_wmax
