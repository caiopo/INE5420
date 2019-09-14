from src.model import Coordinate, Delta


def test_delta_operations():
    c = Coordinate(3, 2)
    d = Delta(10, -5)

    assert c + d == Coordinate(13, -3)
    assert c * d == Coordinate(30, -10)
