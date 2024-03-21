from object import Object


class Point(Object):
    def __init__(self, coordinate_x, coordinate_y, name):
        super().__init__(name, 'Point')
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y