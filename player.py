from character import Personagem
import pygame

class Heroi(Personagem):
    def __init__(self, x, y, largura, altura, vitalidade, velocidade, nome, cor):
        super().__init__(x, y, largura, altura, vitalidade, velocidade, nome, cor)

    def mover(self, teclas):
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:      #direita
            self.x += self.velocidade
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:       #esquerda
            self.x -= self.velocidade
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:       #desce
            self.y += self.velocidade
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:         #sobe
            self.y -= self.velocidade