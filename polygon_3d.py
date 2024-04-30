from object import Object
from point import Point3D


class Polygon3D(Object):
    def __init__(self, coordinates, name, color='black', filled=False):
        super().__init__(name, "Polygon", color)
        self.coordinates = [Point3D(coordinates[i][0], coordinates[i][1], coordinates[i][2], f"Point{i}", color) for i in range(len(coordinates))]
        self.segments = [(self.coordinates[i], self.coordinates[(i + 1) % len(self.coordinates)]) for i in range(len(self.coordinates))]
        self.filled = filled
