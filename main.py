import pygame
from world import Gerador
from player import Heroi
from enemie import Inimigo

pygame.init()
tela = pygame.display.set_mode((800, 600))    #define a resolução do jogo
relogio = pygame.time.Clock()    #cria um relógio para determinar os frame/segundo
gerador = Gerador(300, 500, 20, 20)     #objeto com classe gerador
bob = Heroi(100, 100, 20, 20, 100, 3, 'BOBCleyton', (0,0,255))    #objeto com a classe herói
vilao = Inimigo(600, 400, 20, 20, 100, 1, 'Aluno', (255,0,0))    #objeto com a classe vilão
fonte = pygame.font.Font(None, 72)
texto = fonte.render("GAME OVER", True, (0, 0, 0))

rodando = True
game_over = False
while rodando:    #loop para manter o jogo rodando
    for evento in pygame.event.get():    #aqui guarda tudo que o usuário fizer dentro do jogo
        if evento.type == pygame.QUIT:    #mostra qual o tipo do evento acontecido (que é o de sair do jogo)
            rodando = False     #desliga o loop
    teclas = pygame.key.get_pressed()    #aqui vai ser guardado todos os comandos do teclado
    if not game_over:
        vilao.perseguir(bob)    #envoca o metodo perseguir e chama bob como argumento
        bob.mover(teclas)    #chamando o metodo mover a bob
        if bob.colidiu(vilao):   #caso o boc colida com o aluno
            game_over = True
        if bob.colidiu(gerador):
            gerador.consertar(teclas)
    tela.fill((88, 235, 52))    #apaga os rastros anteriores e pinta o fundo
    gerador.desenhar(tela)
    bob.desenhar(tela)    #bob vai ser desenhado dentro do game
    vilao.desenhar(tela)    #vilao vai ser desenhado dentro do game 
    if game_over:
        tela.blit(texto, ((800 - texto.get_width()) / 2, (600 - texto.get_height()) / 2))   #mostra um texto escrito game over, caso a condição seja True
        if teclas[pygame.K_r]:   #aqui é para reinicio de jogo, caso aperte 'r' o jogo será reiniciado a posição inical
            bob.x = 100
            bob.y = 100
            vilao.x = 600
            vilao.y = 400
            gerador.progresso = 0
            gerador.consertado = False
            game_over = False
    pygame.display.flip()    #o flip serve para mostrar todo resultado dos desenhos
    relogio.tick(60)    #limita a taxa de quadros por segundo
pygame.quit()