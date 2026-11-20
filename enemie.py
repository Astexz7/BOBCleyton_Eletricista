from character import Personagem

class Inimigos(Personagem):
    def __init__(self, x, y, largura, altura, vitalidade, velocidade, nome):
        super().__init__(x, y, largura, altura, vitalidade, velocidade, nome)

aluno = Inimigos('x', 'y', 'l', 'h', 'v', 'vel','Luiz Inácio')
print(aluno.x)
print(aluno.y)
print(aluno.largura)
print(aluno.altura)
print(aluno.vitalidade)
print(aluno.velocidade)
print(aluno.nome)