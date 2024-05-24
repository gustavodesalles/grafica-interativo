from object import Object
from point import Point3D


class BSpline(Object):
    def __init__(self, point_list, name, color):
        super().__init__(name, 'B-Spline', color)
        self.point_list = point_list
        self.point_list_scn = [list(p) for p in point_list]


class BSplineSurface3D(Object):
    def __init__(self, coordinates, name, color):
        super().__init__(name, "BSpline Surface", color)
        self.coordinates = [Point3D(coordinates[i][0], coordinates[i][1], coordinates[i][2], f"Point{i}", color) for i in range(len(coordinates))]
