import pygame

class Gerador:
    def __init__(self, x, y, largura, altura):
        self.x= x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.progresso = 0
        self.consertado = False

    def desenhar(self, tela):
        if self.consertado:
            pygame.draw.rect(tela, (0, 255, 0), (self.x, self.y, self.largura, self.altura))
        else:
            pygame.draw.rect(tela, (255, 255, 0), (self.x, self.y, self.largura, self.altura))


    def consertar(self, teclas):
        if teclas[pygame.K_e]:
            self.progresso += 1
            if self.progresso >= 180:
                self.consertado = True