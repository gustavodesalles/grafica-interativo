class Object:
    def __init__(self, name, type, color):
        self.name = name
        self.type = type
        self.color = color


class Object3D(Object):
    def __init__(self, segmentos=[]):
        self.segmentos = segmentos # lista de segmentos de reta constituídos por um par de Pontos3D
