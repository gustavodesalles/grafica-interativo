from objeto import Objeto


class Reta(Objeto):
    def __init__(self, ponto_inicial, ponto_final, nome):
        super().__init__(nome, 'Reta')
        self.ponto_inicial = ponto_inicial
        self.ponto_final = ponto_final