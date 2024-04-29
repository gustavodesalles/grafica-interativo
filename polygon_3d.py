from object import Object3D


class Polygon3D(Object3D):
    def __init__(self, coordinates, name, color='black', filled=False):
        super().__init__(name)
        self.coordinates = coordinates
        self.color = color
        self.filled = filled
