from typing import List

from src.model import Coordinate, Wireframe


class DisplayFile:
    def __init__(self):
        self.current_id = 0
        self.wireframes = [
            Wireframe(
                'aaaaaaa',
                [
                    Coordinate(100, 200),
                    Coordinate(200, 300),
                    Coordinate(300, 100),
                ]
            )
        ]

    def add(self, coordinates: List[Coordinate]):
        wireframe = Wireframe(
            id=f'wireframe {self.current_id}',
            coordinates=coordinates,
        )
        self.wireframes.append(wireframe)
        self.current_id += 1

    def remove_by_id(self, _id):
        self.wireframes = [
            o
            for o in self.wireframes
            if o.id != _id
        ]

    def reset(self):
        self.__init__()

    def __getitem__(self, id):
        for obj in self.wireframes:
            if obj.id == id:
                return obj

        raise KeyError

    def __iter__(self):
        return iter(self.wireframes)
