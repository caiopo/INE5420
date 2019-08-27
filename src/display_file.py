# from src.entities import Coordinate, Polygon


class DisplayFile:
    def __init__(self):
        self.objects = []

    def add(self, polygon):
        self.objects.append(polygon)

    def remove_by_id(self, _id):
        self.objects = [
            o
            for o in self.objects
            if o.id != _id
        ]
