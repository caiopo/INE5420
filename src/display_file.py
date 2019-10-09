from typing import List

from src.model import Wireframe


class DisplayFile:
    def __init__(self):
        self.wireframes: List[Wireframe] = []
        self.current_id = 0

    def add(self, wireframe: Wireframe):
        if wireframe is not None:
            self.wireframes.append(wireframe)

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

    def next_id(self):
        self.current_id += 1
        return f'{self.current_id - 1}'

    def __getitem__(self, oid):
        for obj in self.wireframes:
            if obj.id == oid:
                return obj

        raise KeyError

    def __iter__(self):
        return iter(self.wireframes)
