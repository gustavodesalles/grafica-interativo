class CoordenadasMundo:
    def __init__(self, xmin, ymin, zmin, xmax, ymax, zmax):
        self.xmin = xmin
        self.ymin = ymin
        self.zmin = zmin
        self.xmax = xmax
        self.ymax = ymax
        self.zmax = zmax

    def coordinates(self):
        return self.xmin, self.ymin, self.zmin, self.xmax, self.ymax, self.zmax