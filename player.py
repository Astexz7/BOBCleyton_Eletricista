from character import Personagem
import pygame

class Heroi(Personagem):
    def __init__(self, x, y, largura, altura, vitalidade, velocidade, nome, cor):
        super().__init__(x, y, largura, altura, vitalidade, velocidade, nome, cor)

    def mover(self, teclas):
        if teclas[pygame.K_RIGHT]:
            self.x += self.velocidade
        if teclas[pygame.K_LEFT]:
            self.x -= self.velocidade