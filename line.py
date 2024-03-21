from object import Object


class Line(Object):
    def __init__(self, start_point, end_point, name):
        super().__init__(name, 'Line')
        self.start_point = start_point
        self.end_point = end_point