class Object:
    def __init__(self, name, obj_type, color):
        self.name = name
        self.type = obj_type
        self.color = color


class Object3D(Object):
    def __init__(self, name, obj_type, color, segments=[]):
        super().__init__(name, obj_type, color)
        self.segments = segments
