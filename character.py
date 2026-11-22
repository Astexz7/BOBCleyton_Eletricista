import pygame

class Personagem:   #essa é a classe pai dos personagens
    def __init__(self, x, y, largura, altura, vitalidade, velocidade, nome, cor):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.vitalidade = vitalidade
        self.velocidade = velocidade
        self.nome = nome
        self.cor = cor

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, self.largura, self.altura))
