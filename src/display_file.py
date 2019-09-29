from typing import List

from src.model import Coordinate, Wireframe


class DisplayFile:
    def __init__(self):
        self.current_id = 0
        self.wireframes: List[Wireframe] = []

    def add(self, coordinates: List[Coordinate]):
        if len(coordinates) == 0:
            return

        wireframe = Wireframe(
            id=f'{self.current_id}',
            coordinates=coordinates,
        )
        self.wireframes.append(wireframe)
        self.current_id += 1

    def remove(self, oid):
        self.wireframes = [
            o
            for o in self.wireframes
            if o.id != oid
        ]

    def replace(self, oid, wireframe):
        for i, w in enumerate(self.wireframes):
            if w.id == oid:
                self.wireframes[i] = wireframe
                break

    def reset(self):
        self.__init__()

    def __getitem__(self, oid):
        for obj in self.wireframes:
            if obj.id == oid:
                return obj

        raise KeyError

    def __iter__(self):
        return iter(self.wireframes)
