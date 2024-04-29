from object import Object, Object3D


class Line(Object):
    def __init__(self, start_point, end_point, name, color):
        super().__init__(name, 'Line', color)
        self.start_point = start_point
        self.end_point = end_point
        self.start_point_scn = list(start_point)
        self.end_point_scn = list(end_point)

class Line3D(Object3D):
    def __init__(self, x1, y1, z1, x2, y2, z2, name, color):
        super().__init__(name, 'Line', color)
        self.start_point = (x1, y1, z1)
        self.end_point = (x2, y2, z2)
        self.start_point_scn = list(self.start_point)
        self.end_point_scn = list(self.end_point)