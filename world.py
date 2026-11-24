import pygame

class Gerador:
    def __init__(self, x, y, largura, altura):
        self.x= x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.progresso = 0
        self.consertado = False
        self.img_quebrado = pygame.image.load("gerador_ruim.png").convert_alpha()
        self.img_quebrado = pygame.transform.scale(self.img_quebrado, (self.largura, self.altura))
        self.img_ligado = pygame.image.load("gerador_bom.png").convert_alpha()
        self.img_ligado = pygame.transform.scale(self.img_ligado, (self.largura, self.altura))

    def desenhar(self, tela):
        if self.consertado:
            tela.blit(self.img_ligado, (self.x, self.y))
        else:
            tela.blit(self.img_quebrado, (self.x, self.y))


    def consertar(self, teclas):
        if teclas[pygame.K_e]:
            self.progresso += 1
            if self.progresso >= 180:
                self.consertado = True