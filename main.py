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
img_mapa = pygame.image.load('mapa.png').convert()
img_mapa = pygame.transform.scale(img_mapa, (800, 600))

relogio = pygame.time.Clock()    #cria um relógio para determinar os frame/segundo

#FASES: cada fase tem uma quantidade de geradores e uma velocidade do aluno
#Fase 1: 4 geradores (um na frente de cada prédio) e aluno com velocidade 1
#Fase 2: + 2 geradores (atrás da UFRPE e atrás do CEAGRI) e aluno com velocidade 2
#Fase 3: + 2 geradores (atrás do CEGOE e atrás do DMV) e aluno com velocidade 2
velocidades_aluno = [1, 2, 2]    #posição 0 = fase 1, posição 1 = fase 2, posição 2 = fase 3

def criar_geradores(numero_fase):
    #devolve uma lista nova de geradores (todos quebrados) de acordo com a fase
    posicoes = [(143, 200), (624, 200), (143, 515), (624, 520)]    #fase 1
    if numero_fase >= 2:
        posicoes = posicoes + [(143, 3), (143, 318)]               #fase 2: soma mais 2 posições
    if numero_fase >= 3:
        posicoes = posicoes + [(624, 3), (624, 318)]               #fase 3: soma mais 2 posições
    lista = []
    for posicao in posicoes:                                       #posicao[0] é o x e posicao[1] é o y
        lista.append(Gerador(posicao[0], posicao[1], 40, 40))      #append coloca o gerador no fim da lista
    return lista

fase = 1                                  #fase atual
fases_liberadas = 1                       #até qual fase o jogador já pode entrar
geradores = criar_geradores(fase)
bob = Heroi(410, 270, 40, 40, 100, 3, 'BOBCleyton', (0,0,255))    #objeto com a classe herói (nasce no caminho central)
vilao = Inimigo(410, 530, 40, 40, 100, velocidades_aluno[fase - 1], 'Aluno', (255,0,0))    #objeto com a classe vilão (nasce embaixo, no caminho central)
vilao.desvio_x = 0    #guardados no próprio aluno: 0 = não está contornando nada
vilao.desvio_y = 0

#PAREDES: um retângulo invisível sobre o corpo de cada prédio (x, y, largura, altura)
paredes = [
    pygame.Rect(55, 45, 210, 105),     #UFRPE
    pygame.Rect(540, 45, 210, 105),    #CEGOE
    pygame.Rect(45, 362, 230, 108),    #CEAGRI
    pygame.Rect(532, 362, 215, 108),   #DMV
]
mostrar_paredes = False    #True mostra as paredes em vermelho (só para testar)

def bate_na_parede(x, y, largura, altura):
    #cria um retângulo com o tamanho recebido na posição (x, y) e confere se encosta em alguma parede
    retangulo = pygame.Rect(x, y, largura, altura)
    for parede in paredes:
        if retangulo.colliderect(parede):
            return True
    return False

def corrigir_parede(personagem, x_antigo, y_antigo):
    #depois que o personagem se moveu, desfaz o movimento do eixo que bateu na parede
    x_novo = personagem.x
    y_novo = personagem.y
    if bate_na_parede(x_novo, y_antigo, personagem.largura, personagem.altura):    #testa só o eixo x
        x_novo = x_antigo
    if bate_na_parede(x_novo, y_novo, personagem.largura, personagem.altura):      #testa o eixo y (com o x já corrigido)
        y_novo = y_antigo
    personagem.x = x_novo
    personagem.y = y_novo

#CONTORNAR PRÉDIOS: evita o aluno ficar preso de cara com a parede quando está alinhado com o bob
def qual_parede(x, y, largura, altura):
    #igual ao bate_na_parede, mas devolve QUAL parede foi atingida (ou None se não bateu em nenhuma)
    retangulo = pygame.Rect(x, y, largura, altura)
    for parede in paredes:
        if retangulo.colliderect(parede):
            return parede
    return None

def passo_livre(aluno, alvo):
    #devolve True se o aluno consegue dar um passo em direção ao alvo sem bater em parede
    x_teste = aluno.x
    y_teste = aluno.y
    if alvo.x > aluno.x:
        x_teste = x_teste + aluno.velocidade
    elif alvo.x < aluno.x:
        x_teste = x_teste - aluno.velocidade
    if alvo.y > aluno.y:
        y_teste = y_teste + aluno.velocidade
    elif alvo.y < aluno.y:
        y_teste = y_teste - aluno.velocidade
    return not bate_na_parede(x_teste, y_teste, aluno.largura, aluno.altura)

def escolher_desvio(aluno, alvo):
    #o aluno ficou preso: escolhe para qual lado vai andar para contornar a parede
    #desvio_x = -1 (esquerda) ou 1 (direita) | desvio_y = -1 (cima) ou 1 (baixo)
    dx = alvo.x - aluno.x
    dy = alvo.y - aluno.y
    if abs(dy) >= abs(dx):                    #queria andar na vertical e bateu: contorna pelo lado
        if dy > 0:
            sinal = 1
        else:
            sinal = -1
        parede = qual_parede(aluno.x, aluno.y + sinal * aluno.velocidade, aluno.largura, aluno.altura)
        if parede is not None:
            if aluno.x + aluno.largura / 2 < parede.centerx:    #está do lado esquerdo da parede: vai pela esquerda
                aluno.desvio_x = -1
            else:
                aluno.desvio_x = 1
    else:                                     #queria andar na horizontal e bateu: contorna por cima ou por baixo
        if dx > 0:
            sinal = 1
        else:
            sinal = -1
        parede = qual_parede(aluno.x + sinal * aluno.velocidade, aluno.y, aluno.largura, aluno.altura)
        if parede is not None:
            if aluno.y + aluno.altura / 2 < parede.centery:     #está acima da parede: vai por cima
                aluno.desvio_y = -1
            else:
                aluno.desvio_y = 1

def mover_aluno(aluno, alvo):
    x_antigo = aluno.x
    y_antigo = aluno.y
    if aluno.desvio_x != 0 or aluno.desvio_y != 0:           #está contornando um prédio
        aluno.x = aluno.x + aluno.desvio_x * aluno.velocidade
        aluno.y = aluno.y + aluno.desvio_y * aluno.velocidade
        corrigir_parede(aluno, x_antigo, y_antigo)
        if aluno.x == x_antigo and aluno.y == y_antigo:      #não saiu do lugar: tenta o outro lado
            aluno.desvio_x = -aluno.desvio_x
            aluno.desvio_y = -aluno.desvio_y
        elif passo_livre(aluno, alvo):                       #o caminho até o bob abriu: volta a perseguir normalmente
            aluno.desvio_x = 0
            aluno.desvio_y = 0
    else:
        aluno.perseguir(alvo)                                #persegue normalmente
        corrigir_parede(aluno, x_antigo, y_antigo)
        if aluno.x == x_antigo and aluno.y == y_antigo:      #não saiu do lugar: ficou preso na parede
            escolher_desvio(aluno, alvo)

fonte = pygame.font.Font(None, 72)
fonte_titulo = pygame.font.Font(None, 80)
fonte_botoes = pygame.font.Font(None, 50)
fonte_botoes_fase = pygame.font.Font(None, 40)

texto_derrota = fonte.render("GAME OVER", True, (255, 0, 111))
texto_vitoria = fonte.render("VICTORY", True, (0, 255, 204))
texto_titulo = fonte_titulo.render("BOBCleyton O Eletricista", True, (255, 255, 0))
texto_jogar = fonte_botoes.render('JOGAR', True, (0, 0, 0))
texto_sair = fonte_botoes.render('SAIR', True, (0,0,0))
texto_fase1 = fonte_botoes_fase.render('FASE 1', True, (0,0,0))
texto_fase2 = fonte_botoes_fase.render('FASE 2', True, (0,0,0))
texto_fase3 = fonte_botoes_fase.render('FASE 3', True, (0,0,0))
texto_voltar = fonte_botoes.render('VOLTAR', True, (0, 0, 0))

botao_jogar = pygame.Rect(290, 280, 220, 50)
botao_sair = pygame.Rect(290, 355, 220, 50)
botao_fase1 = pygame.Rect(100, 200, 150, 150)
botao_fase2 = pygame.Rect(325, 200, 150, 150)
botao_fase3 = pygame.Rect(550, 200, 150, 150)
botao_voltar = pygame.Rect(290, 355, 220, 50)

botoes_fases = [botao_fase1, botao_fase2, botao_fase3]    #lista com os 3 botões de fase
textos_fases = [texto_fase1, texto_fase2, texto_fase3]    #lista com os 3 textos, na mesma ordem

estado = 'menu'
rodando = True
game_over = False
victory = False

while rodando:    #loop para manter o jogo rodando
    if estado == "menu":
        tela.blit(img_menu, (0, 0))
        tela.blit(texto_titulo, ((800 - texto_titulo.get_width()) / 2, 60))
        pygame.draw.rect(tela, (255, 212, 20), botao_jogar)
        pygame.draw.rect(tela, (255, 212, 20), botao_sair)
        tela.blit(texto_jogar, (botao_jogar.x + (botao_jogar.width - texto_jogar.get_width()) / 2, botao_jogar.y + (botao_jogar.height - texto_jogar.get_height()) / 2 + 5))
        tela.blit(texto_sair, (botao_sair.x + (botao_sair.width - texto_sair.get_width()) / 2, botao_sair.y + (botao_sair.height - texto_sair.get_height()) / 2 + 5))

    if estado == 'fases':
        tela.blit(img_menu, (0, 0))
        #desenha os 3 botões: amarelo se a fase está liberada, cinza se está bloqueada
        for i in range(3):                    #i vale 0, 1 e 2 (um por botão)
            if fases_liberadas >= i + 1:      #i + 1 é o número da fase (1, 2 ou 3)
                cor_botao = (255, 212, 20)    #liberada
            else:
                cor_botao = (120, 120, 120)   #bloqueada
            pygame.draw.rect(tela, cor_botao, botoes_fases[i])
            tela.blit(textos_fases[i], (botoes_fases[i].x + (botoes_fases[i].width - textos_fases[i].get_width()) / 2, botoes_fases[i].y + (botoes_fases[i].height - textos_fases[i].get_height()) / 2))

    for evento in pygame.event.get():    #aqui guarda tudo que o usuário fizer dentro do jogo
        if evento.type == pygame.QUIT:    #mostra qual o tipo do evento acontecido (que é o de sair do jogo)
            rodando = False     #desliga o loop
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if estado == 'menu':
                if botao_jogar.collidepoint(evento.pos):
                    estado = 'fases'
                elif botao_sair.collidepoint(evento.pos):
                    rodando = False
            elif estado == 'fases':
                for i in range(3):
                    if botoes_fases[i].collidepoint(evento.pos) and fases_liberadas >= i + 1:    #clicou no botão E a fase está liberada
                        fase = i + 1                                      #guarda qual fase vai jogar
                        geradores = criar_geradores(fase)                 #monta os geradores dessa fase
                        vilao.velocidade = velocidades_aluno[fase - 1]    #velocidade do aluno nessa fase
                        bob.x = 410
                        bob.y = 270
                        vilao.x = 410
                        vilao.y = 530
                        vilao.desvio_x = 0
                        vilao.desvio_y = 0
                        game_over = False
                        victory = False
                        estado = 'jogo'
            elif estado == 'jogo':
                if game_over or victory:
                    if botao_voltar.collidepoint(evento.pos):
                        estado = 'fases'    #volta para a escolha de fases (a próxima já pode estar liberada)

    teclas = pygame.key.get_pressed()    #aqui vai ser guardado todos os comandos do teclado
    if estado == 'jogo':
        if not game_over and not victory:
            #ALUNO: guarda a posição, persegue e corrige se bateu na parede
            mover_aluno(vilao, bob)    #persegue o bob e contorna os prédios se ficar preso

            #BOB: guarda a posição, move e corrige se bateu na parede
            x_antigo = bob.x
            y_antigo = bob.y
            bob.mover(teclas)
            corrigir_parede(bob, x_antigo, y_antigo)

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
                if fase == fases_liberadas and fase < 3:    #venceu a fase mais avançada que tinha liberado...
                    fases_liberadas = fases_liberadas + 1   #...então libera a próxima

        tela.blit(img_mapa, (0, 0))    #pinta o mapa de fundo

        #DESENHO: desenha cada um dos geradores (imagem quebrado ou ligado, escolhida dentro da classe)
        for gerador in geradores:
            gerador.desenhar(tela)

        tela.blit(img_bob, (bob.x, bob.y))
        tela.blit(img_aluno, (vilao.x, vilao.y))

        if mostrar_paredes:    #só para teste: contorno vermelho nas paredes
            for parede in paredes:
                pygame.draw.rect(tela, (255, 0, 0), parede, 2)

        if game_over:
            tela.blit(texto_derrota, ((800 - texto_derrota.get_width()) / 2, (600 - texto_derrota.get_height()) / 2))   #mostra um texto escrito game over, caso a condição seja True
            pygame.draw.rect(tela, (255, 212, 20), botao_voltar)
            tela.blit(texto_voltar, (botao_voltar.x + (botao_voltar.width - texto_voltar.get_width()) / 2, botao_voltar.y + (botao_voltar.height - texto_voltar.get_height()) / 2 + 5))
            if teclas[pygame.K_r]:   #aqui é para reinicio da fase atual, caso aperte 'r'
                bob.x = 410
                bob.y = 270
                vilao.x = 410
                vilao.y = 530
                vilao.desvio_x = 0
                vilao.desvio_y = 0
                geradores = criar_geradores(fase)    #monta de novo os geradores da fase (todos quebrados)
                game_over = False
        if victory:
            tela.blit(texto_vitoria, ((800 - texto_vitoria.get_width()) / 2, (600 - texto_vitoria.get_height()) / 2))   #mostra um texto escrito victory, caso a condição seja True
            pygame.draw.rect(tela, (255, 212, 20), botao_voltar)
            tela.blit(texto_voltar, (botao_voltar.x + (botao_voltar.width - texto_voltar.get_width()) / 2, botao_voltar.y + (botao_voltar.height - texto_voltar.get_height()) / 2 + 5))
            if teclas[pygame.K_r]:   #aqui é para reinicio da fase atual, caso aperte 'r'
                bob.x = 410
                bob.y = 270
                vilao.x = 410
                vilao.y = 530
                vilao.desvio_x = 0
                vilao.desvio_y = 0
                geradores = criar_geradores(fase)
                victory = False
    pygame.display.flip()    #o flip serve para mostrar todo resultado dos desenhos
    relogio.tick(60)    #limita a taxa de quadros por segundo
pygame.quit()