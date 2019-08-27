from typing import List

from src.model import Coordinate, Polygon


class DisplayFile:
    def __init__(self):
        self.current_id = 0
        self.objects = []

    def add(self, coordinates: List[Coordinate]):
        polygon = Polygon(
            id=f'wireframe {self.current_id}',
            coordinates=coordinates,
        )
        self.objects.append(polygon)
        self.current_id += 1

    def remove_by_id(self, _id):
        self.objects = [
            o
            for o in self.objects
            if o.id != _id
        ]

    def reset(self):
        self.__init__()

    def __getitem__(self, id):
        for obj in self.objects:
            if obj.id == id:
                return obj

        raise KeyError

    def __iter__(self):
        return iter(self.objects)
