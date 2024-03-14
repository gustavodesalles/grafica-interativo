class CoordenadasMundo:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def transforma_viewport(self, window, viewport, xw, yw):
        xvp = ((xw - window.xmin)/(window.xmax - window.xmin)) * (viewport.xmax - viewport.xmin)
        yvp = (1 - (yw - window.ymin)/(window.ymax - window.ymin)) * (viewport.ymax - viewport.ymin)
        return xvp, yvp
    