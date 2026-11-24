import pygame

class Gerador:
    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.progresso = 0          #quanto já foi consertado (0 a 180)
        self.consertado = False     #todo gerador começa quebrado

        #carrega as duas imagens uma vez só e ajusta ao tamanho do gerador
        self.img_quebrado = pygame.image.load("gerador_ruim.png").convert_alpha()
        self.img_quebrado = pygame.transform.scale(self.img_quebrado, (self.largura, self.altura))
        self.img_ligado = pygame.image.load("gerador_bom.png").convert_alpha()
        self.img_ligado = pygame.transform.scale(self.img_ligado, (self.largura, self.altura))

    def desenhar(self, tela):
        #escolhe a imagem de acordo com o estado do gerador
        if self.consertado:
            tela.blit(self.img_ligado, (self.x, self.y))
        else:
            tela.blit(self.img_quebrado, (self.x, self.y))

    def consertar(self, teclas):
        if self.consertado:          #se já está consertado, não faz mais nada
            return
        if teclas[pygame.K_e]:       #segurando E, o progresso sobe 1 por quadro
            self.progresso += 1
            if self.progresso >= 180:    #180 quadros = 3 segundos a 60 fps
                self.consertado = True