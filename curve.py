from object import Object


class Curve(Object):
    def __init__(self, point_list, name, color):
        super().__init__(name, 'Curve', color)
        self.point_list = point_list
        self.point_list_scn = [list(p) for p in point_list]