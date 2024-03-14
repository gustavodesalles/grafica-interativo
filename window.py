from coordenadas_mundo import CoordenadasMundo


class Window(CoordenadasMundo):
    def __init__(self, xw_min, yw_min, xw_max, yw_max):
        super().__init__(xw_min, yw_min, xw_max, yw_max)
