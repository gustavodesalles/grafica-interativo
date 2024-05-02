from b_spline import BSpline
from curve import Curve
from line import Line
from point import Point3D
from wireframe import Wireframe
from polygon_3d import Polygon3D

class DisplayFile3D:
    def __init__(self):
        self.objects = {}  # Dicionário para armazenar objetos
        self.counters = {'point': 0, 'line': 0, 'wireframe': 0, 'curve': 0, 'b-spline': 0, 'polygon': 0}  # Contadores para nomeação dos objetos

    def add_point(self, coordinates, color='black'):
        try:
            name = f'Point{self.counters["point"] + 1}'
            point = Point3D(coordinates[0], coordinates[1], coordinates[2], name, color)
            self.objects[name] = point
            self.counters['point'] += 1
        except ValueError:
            print("Invalid coordinates")

    def add_line(self, coordinates, color='black'):
        try:
            name = f'Line{self.counters["line"] + 1}'
            line = Line(coordinates[0], coordinates[1], name, color)
            self.objects[name] = line
            self.counters['line'] += 1
        except ValueError:
            print("Invalid coordinates")

    def add_wireframe(self, coordinates, color='black', filled=False):
        try:
            name = f'Wireframe{self.counters["wireframe"] + 1}'
            wireframe = Wireframe(coordinates, name, color, filled)
            self.objects[name] = wireframe
            self.counters['wireframe'] += 1
        except ValueError:
            print("Invalid coordinates")

    def add_curve(self, coordinates, color='black'):
        try:
            name = f'Curve{self.counters["curve"] + 1}'
            curve = Curve(coordinates, name, color)
            self.objects[name] = curve
            self.counters['curve'] += 1
        except ValueError:
            print("Invalid coordinates")

    def add_b_spline(self, coordinates, color='black'):
        try:
            name = f'BSpline{self.counters["b-spline"] + 1}'
            b_spline = BSpline(coordinates, name, color)
            self.objects[name] = b_spline
            self.counters['b-spline'] += 1
        except ValueError:
            print("Invalid coordinates")

    def add_polygon(self, coordinates, color='black', segments=None):
        try:
            name = f'Polygon{self.counters["polygon"] + 1}'
            polygon = Polygon3D(coordinates, name, color, segments)
            self.objects[name] = polygon
            self.counters['polygon'] += 1
        except ValueError:
            print("Invalid coordinates")
           

    def remove_object(self, name):
        if name in self.objects:
            del self.objects[name]
