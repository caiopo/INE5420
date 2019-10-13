from dataclasses import dataclass


@dataclass
class Color:
    r: float
    g: float
    b: float
    a: float = 1

    def to_list(self):
        return [
            self.r,
            self.g,
            self.b,
            self.a,
        ]


class Colors:
    blue = Color(0, 0, 1, 0.3)
    red = Color(1, 0, 0, 0.3)

    wireframe = Color(0, 0, 0)
    bezier = Color(0.29, 0, 0.5)
    bspline = Color(0, 0.5, 0.5)
