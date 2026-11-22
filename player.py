from character import Personagem

class Heroi(Personagem):
    def __init__(self, x, y, largura, altura, vitalidade, velocidade, nome, cor):
        super().__init__(x, y, largura, altura, vitalidade, velocidade, nome, cor)
