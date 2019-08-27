from src.model import Coordinate, Delta, Size

STEP_SIZE = 100


class Viewport:
    def __init__(self, size: Size):
        self.position = Coordinate(0, 0)
        self.size = size
        self.zoom = 1

    def move(self, delta: Delta):
        self.position += delta * STEP_SIZE / self.zoom
