from coordenadas_mundo import CoordenadasMundo


class Viewport(CoordenadasMundo):
    def __init__(self, xv_min, yv_min, zv_min, xv_max, yv_max, zv_max):
        super().__init__(xv_min, yv_min, zv_min, xv_max, yv_max, zv_max)
