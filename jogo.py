
import math
import random
import pygame

from settings import (
    WIDTH, HEIGHT, TITLE, FPS,
    PLAYER_SIZE, PLAYER_SPEED, WHITE
)

from menu import Menu
from personagens import Jogador, Zombie
from cenario import Cenario, Camera


class Jogo:

    MENU = "menu"
    JOGANDO = "jogando"
    PAUSADO = "pausado"
    GAME_OVER = "fim"

    def __init__(self):

        pygame.init()

        self.tela = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption(TITLE)

        self.relogio = pygame.time.Clock()

        self.fonte = pygame.font.Font(None, 29)
        self.fonte_grande = pygame.font.Font(None, 65)

        self.menu = Menu(self.tela)

        # Instancia o mapa e a câmera
        self.cenario = Cenario()

        self.camera = Camera(
            self.cenario,
            (WIDTH, HEIGHT)
        )

        self.jogador = None

        self.zumbis = pygame.sprite.Group()
        self.tiros = pygame.sprite.Group()

        self.estado = self.MENU
        self.executando = True

        self.pontos = 0

        self.tempo_spawn = 0.0
        self.intervalo_spawn = 1.5

        self.clique_disparo = False
        self.mostrar_hitboxes = False

        # Botões da pausa
        self.botao_continuar = pygame.Rect(
            WIDTH // 2 - 125,
            HEIGHT // 2 - 5,
            250, 58
        )

        self.botao_menu = pygame.Rect(
            WIDTH // 2 - 125,
            HEIGHT // 2 + 75,
            250, 58
        )

    def iniciar_partida(self):

        
        self.jogador = Jogador(
            "Sobrevivente",
            self.cenario.largura / 2,
            self.cenario.altura / 2,
            velocidade=PLAYER_SPEED,
            tamanho=PLAYER_SIZE
        )

        self.zumbis.empty()
        self.tiros.empty()

        self.pontos = 0
        self.tempo_spawn = 0.0

        self.camera.seguir(
            self.jogador.posicao,
            0,
            imediato=True
        )

        self.estado = self.JOGANDO

    def criar_zumbi(self):

        
        if len(self.zumbis) >= 40:
            return

        
        for _ in range(50):

            angulo = random.uniform(
                0,
                math.tau
            )

            raio = random.randint(
                700, 900
            )

            ponto = (
                self.jogador.posicao
                + pygame.Vector2(
                    math.cos(angulo),
                    math.sin(angulo)
                ) * raio
            )

            hitbox = pygame.Rect(
                0, 0, 24, 24
            )

            hitbox.center = (
                round(ponto.x),
                round(ponto.y)
            )

            if not self.cenario.colide_solido(
                hitbox
            ):

                self.zumbis.add(
                    Zombie(ponto)
                )

                return

    def processar_eventos(self):

        self.clique_disparo = False

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                self.executando = False
                continue

            if self.estado == self.MENU:

                acao = self.menu.handle_event(
                    evento
                )

                if acao == "play":
                    self.iniciar_partida()

                elif acao == "quit":
                    self.executando = False

            elif self.estado == self.JOGANDO:

                if (
                    evento.type
                    == pygame.MOUSEBUTTONDOWN
                    and evento.button == 1
                ):
                    self.clique_disparo = True

                if evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_ESCAPE:
                        self.estado = self.PAUSADO

                    elif evento.key == pygame.K_r:

                        self.jogador.arma_equipada.iniciar_recarga()

                    elif evento.key == pygame.K_c:

                        cor = tuple(
                            random.randint(50, 255)
                            for _ in range(3)
                        )

                        self.jogador.trocar_cor(cor)

                    
                    elif evento.key == pygame.K_h:

                        self.mostrar_hitboxes = (
                            not self.mostrar_hitboxes
                        )
                    

                    
                    elif (
                        pygame.K_1
                        <= evento.key
                        <= pygame.K_6
                    ):

                        numero = (
                            evento.key - pygame.K_0
                        )

                        self.jogador.selecionar_arma(
                            numero
                        )

            elif self.estado == self.PAUSADO:

                if (
                    evento.type == pygame.KEYDOWN
                    and evento.key == pygame.K_ESCAPE
                ):
                    self.estado = self.JOGANDO

                elif (
                    evento.type
                    == pygame.MOUSEBUTTONDOWN
                    and evento.button == 1
                ):

                    if self.botao_continuar.collidepoint(
                        evento.pos
                    ):
                        self.estado = self.JOGANDO

                    elif self.botao_menu.collidepoint(
                        evento.pos
                    ):
                        self.estado = self.MENU

            elif self.estado == self.GAME_OVER:

                if evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_r:
                        self.iniciar_partida()

                    elif evento.key == pygame.K_ESCAPE:
                        self.estado = self.MENU

    def atualizar(self, dt):

        if self.estado != self.JOGANDO:
            return

        
        teclas = pygame.key.get_pressed()

        direcao = pygame.Vector2(
            int(teclas[pygame.K_d])
            - int(teclas[pygame.K_a]),

            int(teclas[pygame.K_s])
            - int(teclas[pygame.K_w])
        )

        self.jogador.mover_jogador(
            direcao,
            dt,
            self.cenario
        )

       
        self.camera.seguir(
            self.jogador.posicao,
            dt
        )

        
        destino = self.camera.tela_para_mundo(
            pygame.mouse.get_pos()
        )

        self.jogador.mirar(destino)
        self.jogador.atualizar(dt)

        
        arma = self.jogador.arma_equipada

        disparar = (
            self.clique_disparo
            or (
                arma.automatico
                and pygame.mouse.get_pressed()[0]
            )
        )

        if disparar:

            novos_tiros = self.jogador.disparar(
                destino
            )

            for tiro in novos_tiros:
                self.tiros.add(tiro)

        
        self.tiros.update(
            dt,
            self.cenario
        )

        # 6. SPAWN DOS ZUMBIS
        self.tempo_spawn += dt

        if self.tempo_spawn >= self.intervalo_spawn:

            self.tempo_spawn -= (
                self.intervalo_spawn
            )

            self.criar_zumbi()

        
        self.zumbis.update(
            dt,
            self.jogador,
            self.cenario
        )

       
        for zumbi in list(self.zumbis):

           
            acertos = pygame.sprite.spritecollide(
                zumbi,
                self.tiros,
                dokill=True,

                collided=lambda z, tiro:
                    z.hitbox.colliderect(tiro.rect)
            )

            for tiro in acertos:

                if zumbi.estar_vivo():
                    zumbi.receber_dano(tiro.dano)

                if not zumbi.estar_vivo():

                    zumbi.kill()
                    self.pontos += 1
                    break

            
            if (
                zumbi.alive()
                and zumbi.hitbox.colliderect(
                    self.jogador.hitbox
                )
            ):

                zumbi.atacar(
                    self.jogador
                )

        
        if not self.jogador.estar_vivo():
            self.estado = self.GAME_OVER

    def texto(
        self, mensagem, x, y,
        cor=WHITE
    ):

        imagem = self.fonte.render(
            mensagem, True, cor
        )

        self.tela.blit(
            imagem,
            (x, y)
        )

    def desenhar(self):

        if self.estado == self.MENU:
            self.menu.draw()
            return

        
        self.cenario.desenhar(
            self.tela,
            self.camera
        )

        
        for tiro in self.tiros:

            self.tela.blit(
                tiro.image,
                self.camera.aplicar(
                    tiro.rect
                )
            )

        
        for zumbi in self.zumbis:

            self.tela.blit(
                zumbi.image,
                self.camera.aplicar(
                    zumbi.rect
                )
            )

            """
            if self.mostrar_hitboxes:

                pygame.draw.rect(
                    self.tela,
                    (255, 80, 80),
                    self.camera.aplicar(
                        zumbi.hitbox
                    ),
                    2
                )
                """

        
        self.tela.blit(
            self.jogador.image,
            self.camera.aplicar(
                self.jogador.rect
            )
        )

        """if self.mostrar_hitboxes:

            pygame.draw.rect(
                self.tela,
                (255, 240, 70),
                self.camera.aplicar(
                    self.jogador.hitbox
                ),
                2
            )"""

       
        pygame.draw.rect(
            self.tela,
            (95, 25, 25),
            (18, 18, 220, 18)
        )

        largura_vida = round(
            220 * self.jogador.vida
            / self.jogador.vida_maxima
        )

        pygame.draw.rect(
            self.tela,
            (50, 195, 75),
            (18, 18, largura_vida, 18)
        )

        
        arma = self.jogador.arma_equipada

        if arma.recarregando:
            texto_municao = (
                f"Recarregando {arma.tempo_restante:.1f}s"
            )

        else:
            texto_municao = (
                f"{arma.municao_no_pente}/"
                f"{arma.municao_reserva}"
            )

        self.texto(
            f"HP {self.jogador.vida}/"
            f"{self.jogador.vida_maxima} | "
            f"{arma.nome}: {texto_municao} | "
            f"Dano {arma.dano} | "
            f"Eliminados: {self.pontos}",
            18, 43
        )

        self.texto(
            "1-6: armas | R: recarregar | "
            "C: cor| ESC: pausa",
            18, HEIGHT - 34
        )

        
        if self.estado in (
            self.PAUSADO,
            self.GAME_OVER
        ):

            mascara = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            mascara.fill(
                (0, 0, 0, 190)
            )

            self.tela.blit(
                mascara,
                (0, 0)
            )

            titulo = (
                "JOGO PAUSADO"
                if self.estado == self.PAUSADO
                else "GAME OVER"
            )

            imagem = self.fonte_grande.render(
                titulo,
                True,
                WHITE
            )

            self.tela.blit(
                imagem,
                imagem.get_rect(
                    center=(
                        WIDTH // 2,
                        HEIGHT // 2 - 105
                    )
                )
            )

            if self.estado == self.PAUSADO:

                botoes = [
                    (
                        self.botao_continuar,
                        "CONTINUAR",
                        (45, 145, 72)
                    ),
                    (
                        self.botao_menu,
                        "VOLTAR AO MENU",
                        (145, 55, 55)
                    )
                ]

                for rect, label, cor in botoes:

                    pygame.draw.rect(
                        self.tela,
                        cor,
                        rect,
                        border_radius=8
                    )

                    txt = self.fonte.render(
                        label,
                        True,
                        WHITE
                    )

                    self.tela.blit(
                        txt,
                        txt.get_rect(
                            center=rect.center
                        )
                    )

            else:

                texto = self.fonte.render(
                    "R: reiniciar | ESC: menu",
                    True,
                    WHITE
                )

                self.tela.blit(
                    texto,
                    texto.get_rect(
                        center=(
                            WIDTH // 2,
                            HEIGHT // 2 + 30
                        )
                    )
                )

    def executar(self):

        while self.executando:

            dt = min(
                self.relogio.tick(FPS) / 1000,
                0.05
            )

            self.processar_eventos()
            self.atualizar(dt)
            self.desenhar()

            pygame.display.flip()

        pygame.quit()


def main():
    Jogo().executar()


if __name__ == "__main__":
    main()
