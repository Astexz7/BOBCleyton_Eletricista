from character import Personagem

class Heroi(Personagem):
    def __init__(self, x, y, largura, altura, vitalidade, velocidade, nome):
        super().__init__(x, y, largura, altura, vitalidade, velocidade, nome)

BobCleyton = Heroi('x', 'y', 'l', 'h', 'v', 'vel','BobCleyton')
print(BobCleyton.x)
print(BobCleyton.y)
print(BobCleyton.largura)
print(BobCleyton.altura)
print(BobCleyton.vitalidade)
print(BobCleyton.velocidade)
print(BobCleyton.nome)