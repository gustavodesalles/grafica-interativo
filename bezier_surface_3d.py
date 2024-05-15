from object import Object
from point import Point3D


class BezierSurface3D(Object):
    def __init__(self, coordinates, name, color):
        super().__init__(name, "Bezier Surface", color)
        self.coordinates = [Point3D(coordinates[i][0], coordinates[i][1], coordinates[i][2], f"Point{i}", color) for i in range(len(coordinates))]