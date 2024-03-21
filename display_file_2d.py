from line import Line
from point import Point
from wireframe import Wireframe


class DisplayFile2D:
    def __init__(self):
        self.objects = {}  # Dicionário para armazenar objetos
        self.counters = {'point': 0, 'line': 0, 'wireframe': 0}  # Contadores para nomeação dos objetos

    def add_point(self, coordinates):
        name = f'Ponto{self.counters["point"] + 1}'
        point = Point(coordinates[0], coordinates[1], name)
        self.objects[name] = point
        self.counters['point'] += 1

    def add_line(self, coordinates):
        name = f'Reta{self.counters["line"] + 1}'
        line = Line(coordinates[0], coordinates[1], name)
        self.objects[name] = line
        self.counters['line'] += 1

    def add_wireframe(self, coordinates):
        name = f'Wireframe{self.counters["wireframe"] + 1}'
        wireframe = Wireframe(coordinates, name)
        self.objects[name] = wireframe
        self.counters['wireframe'] += 1

    def remove_object(self, name):
        if name in self.objects:
            del self.objects[name]
