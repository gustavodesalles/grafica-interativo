from object import Object


class Line(Object):
    def __init__(self, start_point, end_point, name, color):
        super().__init__(name, 'Line', color)
        self.start_point = start_point
        self.end_point = end_point
        self.start_point_scn = list(start_point)
        self.end_point_scn = list(end_point)