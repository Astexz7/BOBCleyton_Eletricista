# BOBCleyton O Eletricista

Jogo 2D em Python, visto de cima (top-down), desenvolvido como atividade da faculdade (Bacharelado em Sistemas de Informação, UFRPE).

**Autores:** Lucas Holanda, Festo Murilo e Nicolas Rodrigues
**Disciplina:** Princípios de Programação

## Sobre o jogo

O campus ficou sem energia e as aulas pararam. O eletricista **Bob** precisa consertar os geradores de cada departamento (UFRPE, CEGOE, CEAGRI e DMV) para reacender a luz e as aulas voltarem ao normal. Só que um **aluno** o persegue para impedi-lo.

- **Vitória:** consertar todos os geradores da fase.
- **Derrota:** ser tocado pelo aluno.

### Controles

| Ação | Tecla / mouse |
|---|---|
| Andar | Setas ou **W A S D** |
| Consertar um gerador | Segurar **E** encostado nele (3 segundos) |
| Reiniciar a fase atual | **R** (após GAME OVER ou VICTORY) |
| Menus e botões | Clique do mouse |

### Fases

| Fase | Geradores | Velocidade do aluno | Como libera |
|---|---|---|---|
| 1 | 4 (um na frente de cada prédio) | 1 | Liberada desde o início |
| 2 | 6 (+2: atrás da UFRPE e atrás do CEAGRI) | 2 | Vencer a fase 1 |
| 3 | 8 (+2: atrás do CEGOE e atrás do DMV) | 2 | Vencer a fase 2 |

## Tecnologias e bibliotecas

| Item | Versão usada | Justificativa |
|---|---|---|
| **Python** | 3.14 | Linguagem da atividade. |
| **pygame-ce** | 2.5.8 | Biblioteca para jogos 2D: janela, laço de jogo, desenho de imagens e formas, fontes, eventos de teclado e mouse e colisão com `pygame.Rect`. Foi escolhida a edição da comunidade (*Community Edition*) porque o pacote `pygame` tradicional não instalou no Python 3.14 (o `pip` tentou compilar e falhou). O código continua usando `import pygame`, sem nenhuma alteração. |

Não foi usada nenhuma outra biblioteca externa nem módulos extras da biblioteca padrão. Toda a lógica (estados, fases, colisão e perseguição) foi escrita no próprio projeto.

## Como instalar e rodar

Pré-requisito: Python 3 instalado, com a opção **Add Python to PATH** marcada na instalação.

```
git clone https://github.com/Astexz7/BOBCleyton_Eletricista.git
cd BOBCleyton_Eletricista
pip install pygame-ce
python main.py
```

Instale apenas o `pygame-ce`. Ele **não deve ser instalado junto** com o `pygame` tradicional, pois os dois usam o mesmo nome de importação e entram em conflito (se já instalou o outro, rode `pip uninstall pygame` antes).

Execute o `python main.py` **de dentro da pasta do projeto**, pois as imagens são carregadas por caminho relativo.

## Importações necessárias

Cada módulo importa apenas o que usa:

```python
# main.py
import pygame
from world import Gerador
from player import Heroi
from enemie import Inimigo

# player.py e enemie.py
from character import Personagem

# character.py e world.py
import pygame
```

## Organização dos módulos

```
BOBCleyton_Eletricista/
├── main.py          # laço principal, estados (menu, fases, jogo), fases, paredes e telas
├── character.py     # classe Personagem (classe pai)
├── player.py        # classe Heroi (o Bob)
├── enemie.py        # classe Inimigo (o aluno)
├── world.py         # classe Gerador
├── bob.png          # imagem do Bob
├── aluno.png        # imagem do aluno
├── gerador_ruim.png # gerador quebrado
├── gerador_bom.png  # gerador consertado
├── menu.png         # fundo do menu e da seleção de fases
└── mapa.png         # mapa do campus
```

| Módulo | Responsabilidade |
|---|---|
| `character.py` | `Personagem`: guarda posição (`x`, `y`), tamanho (`largura`, `altura`), `vitalidade`, `velocidade`, `nome` e `cor`. Possui `desenhar(tela)` e `colidiu(outro)`, que compara dois `pygame.Rect`. |
| `player.py` | `Heroi(Personagem)`: método `mover(teclas)`, que lê as setas e WASD e mantém o Bob dentro da janela. |
| `enemie.py` | `Inimigo(Personagem)`: método `perseguir(alvo)`, que dá um passo na direção do alvo. |
| `world.py` | `Gerador`: guarda o `progresso` do conserto e se está `consertado`. Escolhe a imagem (quebrado ou ligado) e conserta quando o progresso chega a 180 quadros (3 segundos a 60 FPS). |
| `main.py` | Carrega os recursos, controla os estados do jogo, cria as fases, trata colisão com as paredes e roda o laço principal a 60 FPS. |

### Conceitos de programação aplicados

- **Herança:** `Heroi` e `Inimigo` herdam de `Personagem` com `super().__init__(...)`, reaproveitando atributos e métodos (`desenhar`, `colidiu`).
- **Encapsulamento por módulos:** cada arquivo cuida de uma parte do jogo.
- **Máquina de estados:** a variável `estado` (`menu`, `fases`, `jogo`) define qual tela é exibida e quais cliques valem.
- **Listas e laços:** os geradores ficam numa lista e são desenhados, consertados e verificados com `for`. A fase define quantos geradores a lista terá.

## Funcionalidades de inovação

1. **Aluno que contorna obstáculos.** Em jogos simples, o inimigo que persegue em linha reta fica travado de cara com qualquer parede. Aqui, quando o aluno percebe que não saiu do lugar, ele identifica a parede que o bloqueia, escolhe o lado mais próximo da ponta do prédio, caminha de lado até o caminho até o Bob abrir e então volta a perseguir (`mover_aluno`, `escolher_desvio` e `passo_livre`, em `main.py`). Isso foi feito sem bibliotecas de busca de caminho.
2. **Colisão com deslizamento.** O movimento é conferido separadamente nos eixos X e Y (`corrigir_parede`). Ao bater de lado, o personagem desliza pela parede em vez de travar. A mesma função serve para o Bob e para o aluno.
3. **Mapa do campus com mecânica própria.** Os prédios (UFRPE, CEGOE, CEAGRI e DMV) têm paredes invisíveis e geradores posicionados na frente ou atrás deles, e a dificuldade cresce por fase (mais geradores e aluno mais rápido), com desbloqueio progressivo.

## Recursos visuais

O mapa, o menu e as imagens dos personagens e dos geradores foram gerados com ferramenta de inteligência artificial (ChatGPT) e ajustados para o tamanho do jogo com `pygame.transform.scale`.

