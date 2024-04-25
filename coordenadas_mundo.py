class CoordenadasMundo:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def coordinates(self):
        return self.xmin, self.ymin, self.xmax, self.ymax
    