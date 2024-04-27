from object import Object, Object3D


class Point(Object):
    def __init__(self, coordinate_x, coordinate_y, name, color):
        super().__init__(name, 'Point', color)
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.coordinate_x_scn = coordinate_x
        self.coordinate_y_scn = coordinate_y


class Point3D(Object3D):
    def __init__(self, coordinate_x, coordinate_y, coordinate_z, name, color):
        super().__init__(name, 'Point', color)
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.coordinate_z = coordinate_z
        self.coordinate_x_scn = coordinate_x
        self.coordinate_y_scn = coordinate_y
        self.coordinate_z_scn = coordinate_z