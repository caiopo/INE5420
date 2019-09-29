from enum import Enum, auto
from typing import List

from src.model import Coordinate, Wireframe

CENTER = 0  # 0000
LEFT = 1  # 0001
RIGHT = 2  # 0010
BOTTOM = 4  # 0100
TOP = 8  # 1000


class Clipper:
    def __init__(self, vmin: Coordinate, vmax: Coordinate):
        self.vmin = vmin
        self.vmax = vmax

    def clip(self, wireframe: Wireframe) -> List[Wireframe]:
        wlen = len(wireframe.coordinates)

        if wlen == 1:
            inside, coord = self.clip_point(wireframe.coordinates[0])
            if not inside:
                return []

            return [
                wireframe.copy(
                    coordinates=[coord],
                )
            ]

        if wlen == 2:
            inside, c0, c1 = self.cohen_sutherland(*wireframe.coordinates)
            if not inside:
                return []

            return [
                wireframe.copy(
                    coordinates=[c0, c1],
                )
            ]

        assert wlen > 2

        return self.weiler_atherton(wireframe)

    def inside(self, coord: Coordinate):
        return (self.vmin.x <= coord.x <= self.vmax.x
                and self.vmin.y <= coord.y <= self.vmax.y)

    def clip_point(self, coord: Coordinate):
        if self.inside(coord):
            return True, coord
        return False, None

    def cohen_sutherland(self, c0: Coordinate, c1: Coordinate):
        while True:
            code0 = self._code(c0)
            code1 = self._code(c1)

            if (code0 | code1) == 0:
                return True, c0, c1

            elif (code0 & code1) != 0:
                return False, None, None

            else:
                out = code0 if code0 != 0 else code1

                x = None
                y = None

                if (out & TOP) != 0:
                    x = c0.x + (c1.x - c0.x) * (self.vmin.y - c0.y) / (c1.y - c0.y)
                    y = self.vmin.y

                elif (out & BOTTOM) != 0:
                    x = c0.x + (c1.x - c0.x) * (self.vmax.y - c0.y) / (c1.y - c0.y)
                    y = self.vmax.y

                elif (out & RIGHT) != 0:
                    x = self.vmax.x
                    y = c0.y + (c1.y - c0.y) * (self.vmax.x - c0.x) / (c1.x - c0.x)

                elif (out & LEFT) != 0:
                    x = self.vmin.x
                    y = c0.y + (c1.y - c0.y) * (self.vmin.x - c0.x) / (c1.x - c0.x)

                assert x is not None and y is not None

                if out == code0:
                    c0 = Coordinate(x, y)
                else:
                    c1 = Coordinate(x, y)

    def weiler_atherton(self, wireframe: Wireframe):
        subject = [(c, _Type.ORIGINAL) for c in wireframe.coordinates]

        # for s in enumerate(subject):
        #     print(s)
        #
        # print()

        for i, (c0, c1) in enumerate(wireframe.lines):
            inside, nc0, nc1 = self.cohen_sutherland(c0, c1)

            # print(i, c0, c1, nc0, nc1)

            if inside:
                if c1 != nc1:
                    index = subject.index((c0, _Type.ORIGINAL))
                    subject.insert(index + 1, (nc1, _Type.EXITING))

                if c0 != nc0:
                    index = subject.index((c0, _Type.ORIGINAL))
                    subject.insert(index + 1, (nc0, _Type.ENTERING))

        out = []

        current = None

        for s in enumerate(subject):
            print(s)
        print()

        for first_iteration, (c, t) in _cycle(subject):
            if t == _Type.ENTERING:
                current = [c]

            if current is not None:
                if self.inside(c):
                    current.append(c)

                if t == _Type.EXITING:
                    out.append(current)
                    current = None

            if not first_iteration and current is None:
                break

        if len(out) == 0 and self.inside(subject[0][0]):
            return [wireframe]

        return [
            wireframe.copy(coordinates=c)
            for c in out
        ]

    def _code(self, coord: Coordinate):
        code = CENTER

        if coord.x < self.vmin.x:
            code |= LEFT
        elif coord.x > self.vmax.x:
            code |= RIGHT

        if coord.y < self.vmin.y:
            code |= TOP
        elif coord.y > self.vmax.y:
            code |= BOTTOM

        return code


class _Type(Enum):
    ORIGINAL = auto()
    ENTERING = auto()
    EXITING = auto()


def _cycle(lst):
    i = 0
    size = len(lst)

    while True:
        yield (i < (size * 2)), lst[i % size]
        i += 1
