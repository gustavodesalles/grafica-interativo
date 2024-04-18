from object import Object


class Curve(Object):
    def __init__(self, p1, p2, p3, p4, name, color):
        super().__init__(name, 'Curve', color)
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p1_scn = p1
        self.p2_scn = p2
        self.p3_scn = p3
        self.p4_scn = p4