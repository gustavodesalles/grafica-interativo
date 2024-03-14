from objeto import Objeto


class Ponto(Objeto):
    def __init__(self, coordenada_x, coordenada_y, nome):
        super().__init__(nome, 'Ponto')
        self.coordenada_x = coordenada_x
        self.coordenada_y = coordenada_y