from object import Object
from point import Point3D


class Polygon3D(Object):
    def __init__(self, coordinates, name, color='black', segments=None):
        super().__init__(name, "Polygon", color)
        self.coordinates = [Point3D(coordinates[i][0], coordinates[i][1], coordinates[i][2], f"Point{i}", color) for i in range(len(coordinates))]

        if segments is None:
            self.segments = [(self.coordinates[i], self.coordinates[(i + 1) % len(self.coordinates)]) for i in range(len(self.coordinates))]
        else:
            # self.segments = segments
            self.segments = [(self.coordinates[segment[0] - 1], self.coordinates[segment[1] - 1]) for segment in segments]

