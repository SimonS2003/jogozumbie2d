# 🧟 Zombie Survival 2D

**Zombie Survival 2D** é um protótipo de jogo de sobrevivência com visão de cima, desenvolvido em Python com Pygame. Você controla um sobrevivente, explora um mapa em pixel art e tenta eliminar o maior número de zumbis antes que sua vida acabe.

O projeto também serve como exercício de programação orientada a objetos. Personagens, armas, projéteis, cenário e câmera têm responsabilidades próprias. A classe `Jogo` reúne essas partes para executar a partida.

## Como instalar e executar

Você precisa do **Python 3**, do **pip** e de um ambiente com interface gráfica para abrir a janela. A dependência do jogo é o [pygame-ce](https://pypi.org/project/pygame-ce/), importado no código como `pygame`.

Com o Git instalado, baixe o projeto e entre na pasta.

```bash
git clone https://github.com/leehsantos13/jogozumbie2d.git
cd jogozumbie2d
```

Você também pode usar **Code → Download ZIP** no GitHub, extrair o arquivo e abrir um terminal na pasta que contém `jogo.py`.

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install pygame-ce
.\.venv\Scripts\python.exe jogo.py
```

### Linux e macOS

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install pygame-ce
./.venv/bin/python jogo.py
```

Se aparecer `ModuleNotFoundError: No module named 'pygame'`, verifique se instalou o `pygame-ce` com o mesmo interpretador Python usado para executar `jogo.py`. Os comandos acima usam o Python do ambiente virtual nas duas etapas.

## Como jogar

1. Clique em **Jogar** no menu principal.
2. Mova-se pelo mapa, mire com o mouse e dispare contra os zumbis. A água e as pedras bloqueiam a passagem. Procure a ponte para atravessar o rio.
3. Acompanhe no painel a vida, a arma equipada, a munição, o dano da arma e o total de zumbis eliminados.
4. Quando a vida chega a zero, a partida termina. Pressione **R** para reiniciar ou **Esc** para voltar ao menu.

### Controles

| Controle | Ação |
| --- | --- |
| **W**, **A**, **S**, **D** | Mover o sobrevivente |
| **Mouse** | Mirar |
| **Botão esquerdo do mouse** | Disparar. Mantenha pressionado nas armas automáticas |
| **1** a **6** | Trocar de arma |
| **R** | Recarregar durante a partida ou reiniciar na tela de fim de jogo |
| **C** | Sortear uma nova cor para o sobrevivente |
| **Esc** | Pausar, retomar ou voltar ao menu na tela de fim de jogo |

### Armas

O sobrevivente começa com a **MP5** equipada. Cada arma tem seus próprios valores de dano, cadência, alcance, peso, munição e tempo de recarga. A troca preserva a munição de cada arma, e o peso da arma equipada afeta a velocidade do personagem.

| Tecla | Arma | Categoria | Dano por projétil | Disparo |
| --- | --- | --- | ---: | --- |
| **1** | MP5 | Submetralhadora | 20 | Automático |
| **2** | M8A1 | Fuzil de assalto | 36 | Semiautomático |
| **3** | Balista | Fuzil de precisão | 95 | Semiautomático |
| **4** | LSAT | Metralhadora leve | 25 | Automático |
| **5** | RM870 | Escopeta | 13 | Semiautomático, com seis projéteis por disparo |
| **6** | Five-Seven | Pistola | 26 | Semiautomático |

## Como o jogo funciona

### Mapa, câmera e pixel art

O cenário tem **80 × 60 blocos** de 40 pixels, formando um mapa de **3.200 × 2.400 pixels**. Ele inclui grama, terra, pedras, um rio e uma ponte. As texturas do chão e os sprites dos personagens e das armas são desenhados no código com `pygame.PixelArray`.

A câmera acompanha o sobrevivente com movimento suave e respeita os limites do mapa. O jogo guarda as posições em coordenadas do mundo e aplica o deslocamento da câmera ao desenhar. Ao mirar, faz a conversão inversa e transforma a posição do mouse na janela em um ponto no mundo.

### Zumbis, colisões e dano

O jogo tenta criar um zumbi a cada **1,5 segundo**, com um limite de **40 simultâneos**. Quando encontra um ponto válido, o zumbi aparece a **700–900 pixels** do sobrevivente. Fora do raio de detecção, os zumbis sorteiam uma direção em intervalos de **1 a 3 segundos**. Quando o jogador está a até **250 pixels**, passam a se mover na direção dele. A detecção usa a distância, e o terreno sólido bloqueia o deslocamento.

As colisões usam retângulos chamados **hitboxes**. Um projétil que acerta a hitbox de um zumbi causa dano. Quando as hitboxes do zumbi e do sobrevivente se sobrepõem, o zumbi ataca. Depois de sofrer dano, o sobrevivente fica invulnerável por **0,8 segundo**, o que evita perder vida a cada quadro de contato. Cada zumbi eliminado soma um ponto.

### Laço principal

A cada quadro, a classe `Jogo` processa os eventos de teclado e mouse, atualiza a simulação e desenha o estado atual. Os movimentos usam `dt`, o tempo entre quadros, para manter a velocidade dos objetos consistente com variações na taxa de quadros.

## Estrutura do projeto

| Arquivo | Responsabilidade |
| --- | --- |
| [`jogo.py`](jogo.py) | Ponto de entrada da versão gráfica. A classe `Jogo` controla a partida, os eventos, a criação de zumbis, as colisões e o desenho da interface. |
| [`personagens.py`](personagens.py) | `Boneco` reúne atributos e comportamentos como vida, dano e movimento. `Jogador` herda de `Boneco` e gerencia o arsenal. `Zombie` herda de `Inimigo`, que implementa a movimentação aleatória e a perseguição. |
| [`armas.py`](armas.py) | `Arma` centraliza o disparo, a recarga e a munição. As subclasses representam as categorias de armas e os seis modelos do arsenal. |
| [`entities/bullet.py`](entities/bullet.py) | A classe `Bullet` move o projétil e o remove ao atingir o alcance máximo ou colidir com o terreno sólido. |
| [`cenario.py`](cenario.py) | `Cenario` gera o terreno e verifica obstáculos. `Camera` acompanha o jogador e converte posições entre a tela e o mundo. |
| [`menu.py`](menu.py) | A classe `Menu` desenha a tela inicial e trata os cliques nos botões **Jogar** e **Sair**. |
| [`settings.py`](settings.py) | Define as dimensões da janela, o limite de FPS, as cores e os valores de tamanho e velocidade base do jogador. |
| [`main.py`](main.py) | Protótipo antigo de combate pelo terminal. Para abrir a versão gráfica, use `jogo.py`. |
