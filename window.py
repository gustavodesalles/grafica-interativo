from coordenadas_mundo import CoordenadasMundo


class Window(CoordenadasMundo):
    def __init__(self, xw_min, yw_min, zw_min, xw_max, yw_max, zw_max):
        super().__init__(xw_min, yw_min, zw_min, xw_max, yw_max, zw_max)

    def get_wc(self):
        wcx = (self.xmin + self.xmax) / 2
        wcy = (self.ymin + self.ymax) / 2
        wcz = (self.zmin + self.zmax) / 2
        return wcx, wcy, wcz
