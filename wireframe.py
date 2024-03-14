from objeto import Objeto


class Wireframe(Objeto):
    def __init__(self, nome):
        super().__init__(nome, 'Wireframe')
        self.lista_pontos = []
        