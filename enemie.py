from character import Personagem

class Inimigo(Personagem):
    def __init__(self, x, y, largura, altura, vitalidade, velocidade, nome, cor):
        super().__init__(x, y, largura, altura, vitalidade, velocidade, nome, cor)

    def perseguir(self, alvo):      #metodo que vai perseguir o bob
        if alvo.x > self.x:
            self.x += self.velocidade
        if alvo.x < self.x:
            self.x -= self.velocidade
        if alvo.y > self.y:
            self.y += self.velocidade
        if alvo.y < self.y:
            self.y -= self.velocidade