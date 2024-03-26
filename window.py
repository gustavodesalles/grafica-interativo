from coordenadas_mundo import CoordenadasMundo


class Window(CoordenadasMundo):
    def __init__(self, xw_min, yw_min, xw_max, yw_max):
        super().__init__(xw_min, yw_min, xw_max, yw_max)
        self.xmin_ppc = xw_min
        self.ymin_ppc = yw_min
        self.xmax_ppc = xw_max
        self.ymax_ppc = yw_max
