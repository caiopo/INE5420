from src.model import Coordinate, Polygon


class DisplayFile:
    def __init__(self):
        self.objects = [
            Polygon(
                '0',
                [
                    Coordinate(400, 500)
                ],
            ),
            Polygon(
                '1',
                [
                    Coordinate(10, 100),
                    Coordinate(100, 300)
                ],
            )

        ]

    def add(self, polygon):
        self.objects.append(polygon)

    def remove_by_id(self, _id):
        self.objects = [
            o
            for o in self.objects
            if o.id != _id
        ]

    def __getitem__(self, id):
        for obj in self.objects:
            if obj.id == id:
                return obj

        raise KeyError

    def __iter__(self):
        return iter(self.objects)
