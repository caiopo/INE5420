from src.model import Coordinate


def almost_equal(c1: Coordinate, c2: Coordinate, threshold=0.01):
    return abs(c1.x - c2.x) < threshold and abs(c1.y - c2.y) < threshold
