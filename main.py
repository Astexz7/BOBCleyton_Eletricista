import pygame
from world import Gerador
from player import Heroi
from enemie import Inimigo

pygame.init()
tela = pygame.display.set_mode((800, 600))    #define a resolução do jogo

    #Aqui são guardadas todas as imagens e escaladas de acordo com sua resolução
img_bob = pygame.image.load("bob.png").convert_alpha()
img_bob = pygame.transform.scale(img_bob, (40, 40))
img_aluno = pygame.image.load("aluno.png").convert_alpha()
img_aluno = pygame.transform.scale(img_aluno, (40, 40))
img_menu = pygame.image.load('menu.png').convert()
img_menu = pygame.transform.scale(img_menu, (800, 600))

relogio = pygame.time.Clock()    #cria um relógio para determinar os frame/segundo

#LISTA com os 3 geradores (um por departamento). "geradores" (plural) é a lista inteira
geradores = [Gerador(50, 50, 40, 40), Gerador(700, 50, 40, 40), Gerador(375, 500, 40, 40)]

bob = Heroi(100, 100, 40, 40, 100, 3, 'BOBCleyton', (0,0,255))    #objeto com a classe herói
vilao = Inimigo(600, 400, 40, 40, 100, 1, 'Aluno', (255,0,0))    #objeto com a classe vilão
fonte = pygame.font.Font(None, 72)
texto_derrota = fonte.render("GAME OVER", True, (255, 0, 111))
texto_vitoria = fonte.render("VICTORY", True, (0, 255, 204))
fonte_titulo = pygame.font.Font(None, 80)
texto_titulo = fonte_titulo.render("BOBCleyton O Eletricista", True, (255, 255, 0))
botao_jogar = pygame.Rect(300, 277, 200, 60)


estado = 'menu'
rodando = True
game_over = False
victory = False
while rodando:    #loop para manter o jogo rodando
    if estado == "menu":
        tela.blit(img_menu, (0, 0))
        tela.blit(texto_titulo, ((800 - texto_titulo.get_width()) / 2, 60))
        pygame.draw.rect(tela, (255, 255, 255), botao_jogar)
    for evento in pygame.event.get():    #aqui guarda tudo que o usuário fizer dentro do jogo
        if evento.type == pygame.QUIT:    #mostra qual o tipo do evento acontecido (que é o de sair do jogo)
            rodando = False     #desliga o loop
    teclas = pygame.key.get_pressed()    #aqui vai ser guardado todos os comandos do teclado
    if estado == 'jogo':
        if not game_over and not victory:
            vilao.perseguir(bob)    #envoca o metodo perseguir e chama bob como argumento
            bob.mover(teclas)    #chamando o metodo mover a bob
            if bob.colidiu(vilao):   #caso o bob colida com o aluno
                game_over = True

            #CONSERTO: o for pega UM gerador por vez da lista ("gerador" no singular)
            for gerador in geradores:
                if bob.colidiu(gerador):          #se o bob está encostado NESSE gerador...
                    gerador.consertar(teclas)     #...segurando E, o progresso DELE sobe

            #VITÓRIA: só vale se TODOS os geradores estiverem consertados
            todos_consertados = True              #começa achando que todos estão consertados
            for gerador in geradores:
                if not gerador.consertado:        #se encontrar UM que não está consertado...
                    todos_consertados = False     #...então nem todos estão
            if todos_consertados:                 #só chega aqui se nenhum estava quebrado
                victory = True

        tela.fill((88, 235, 52))    #apaga os rastros anteriores e pinta o fundo

        #DESENHO: desenha cada um dos 3 geradores (imagem quebrado ou ligado, escolhida dentro da classe)
        for gerador in geradores:
            gerador.desenhar(tela)

        tela.blit(img_bob, (bob.x, bob.y))
        tela.blit(img_aluno, (vilao.x, vilao.y))
        if game_over:
            tela.blit(texto_derrota, ((800 - texto_derrota.get_width()) / 2, (600 - texto_derrota.get_height()) / 2))   #mostra um texto escrito game over, caso a condição seja True
            if teclas[pygame.K_r]:   #aqui é para reinicio de jogo, caso aperte 'r' o jogo será reiniciado a posição inical
                bob.x = 100
                bob.y = 100
                vilao.x = 600
                vilao.y = 400
                #RESET: volta cada gerador ao estado inicial (quebrado e sem progresso)
                for gerador in geradores:
                    gerador.progresso = 0
                    gerador.consertado = False
                game_over = False
        if victory:
            tela.blit(texto_vitoria, ((800 - texto_vitoria.get_width()) / 2, (600 - texto_vitoria.get_height()) / 2))   #mostra um texto escrito victory, caso a condição seja True
            if teclas[pygame.K_r]:   #aqui é para reinicio de jogo, caso aperte 'r' o jogo será reiniciado a posição inical
                bob.x = 100
                bob.y = 100
                vilao.x = 600
                vilao.y = 400
                for gerador in geradores:
                    gerador.progresso = 0
                    gerador.consertado = False
                victory = False
    pygame.display.flip()    #o flip serve para mostrar todo resultado dos desenhos
    relogio.tick(60)    #limita a taxa de quadros por segundo
pygame.quit()