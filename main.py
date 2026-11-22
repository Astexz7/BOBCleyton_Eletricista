import pygame
from player import Heroi
from enemie import Inimigo

pygame.init()
tela = pygame.display.set_mode((800, 600))    #define a resolução do jogo
relogio = pygame.time.Clock()   #cria um relógio para determinar os frame/segundo
bob = Heroi(100, 100, 40, 40, 100, 5, 'BOBCleyton', (0,0,255)) #objeto com a classe herói
vilao = Inimigo(600, 400, 40, 40, 100, 5, 'Aluno', (255,0,0))   #objeto com a classe vilão

rodando = True
while rodando:  #loop para manter o jogo rodando
    for evento in pygame.event.get():    #aqui guarda tudo que o usuário fizer dentro do jogo
        if evento.type == pygame.QUIT:  #mostra qual o tipo do evento acontecido (que é o de sair do jogo)
            rodando = False     #desliga o loop
    teclas = pygame.key.get_pressed()   #aqui vai ser guardado todos os comandos do teclado
    bob.mover(teclas)   #chamando o metodo mover a bob
    tela.fill((52, 235, 94))    #apaga os rastros anteriores e pinta o fundo
    bob.desenhar(tela)  #bob vai ser desenhado dentro do game
    vilao.desenhar(tela)    #vilao vai ser desenhado dentro do game 
    pygame.display.flip()   #o flip serve para mostrar todo resultado dos desenhos
    relogio.tick(60)    #limita a taxa de quadros por segundo
pygame.quit()