from object import Object


class Wireframe(Object):
    def __init__(self, name):
        super().__init__(name, 'Wireframe')
        self.point_list = []

    def __init__(self, point_list, name):
        super().__init__(name, 'Wireframe')
        self.point_list = point_list
        self.point_list_scn = [list(p) for p in point_list]
