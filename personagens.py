from abc import ABC, abstractmethod
import math
import random
import pygame

from armas import (
    MP5, M8A1, Balista,
    LSAT, RM870, FiveSeven
)


class Boneco(pygame.sprite.Sprite, ABC):
    

    def __init__(
        self, nome, x, y,
        vida=100, armadura=0, dano=5,
        velocidade=100,
        cor_base=(0, 140, 255),
        tamanho=40
    ):
        super().__init__()

        self.nome = nome
        self.posicao = pygame.Vector2(x, y)

        self.vida = vida
        self.vida_maxima = vida

        self.armadura = armadura
        self.dano = dano
        self.velocidade = velocidade

        self.cor_base = cor_base
        self.tamanho = tamanho

        self.angulo = 0.0
        self.tempo_efeito_dano = 0.0

        
        self.hitbox = pygame.Rect(
            0, 0,
            int(tamanho * 0.60),
            int(tamanho * 0.60)
        )

        self.hitbox.center = (
            round(x),
            round(y)
        )

        self.imagem_original = pygame.Surface(
            (tamanho, tamanho),
            pygame.SRCALPHA
        )

        self.gerar_sprite_pixelarray()

        self.imagem_atual = (
            self.imagem_original.copy()
        )

        self.image = self.imagem_atual.copy()

        self.rect = self.image.get_rect(
            center=self.hitbox.center
        )

    def gerar_sprite_pixelarray(self):

        t = self.tamanho

        self.imagem_original.fill(
            (0, 0, 0, 0)
        )

        with pygame.PixelArray(
            self.imagem_original
        ) as p:

            # Corpo
            p[6:18, 4:t-4] = self.cor_base

            # Braços
            p[16:28, 7:12] = (230, 190, 150)
            p[16:28, t-12:t-7] = (230, 190, 150)

            # Cabeça
            p[8:22, 9:t-9] = (240, 200, 160)

            # Olhos
            p[18:21, 11:14] = (20, 20, 20)
            p[18:21, t-14:t-11] = (20, 20, 20)

    def trocar_cor(self, nova_cor):

        self.cor_base = nova_cor

        self.gerar_sprite_pixelarray()

        self.imagem_atual = (
            self.imagem_original.copy()
        )

    def estar_vivo(self):
        return self.vida > 0

    def receber_dano(self, quantidade):

        if (
            quantidade <= 0
            or not self.estar_vivo()
        ):
            return False

        dano_efetivo = max(
            1,
            quantidade - self.armadura
        )

        self.vida = max(
            0,
            self.vida - dano_efetivo
        )

        
        self.imagem_atual = (
            self.imagem_original.copy()
        )

        with pygame.PixelArray(
            self.imagem_atual
        ) as p:

            p.replace(
                self.cor_base,
                (245, 65, 65)
            )

        self.tempo_efeito_dano = 0.16

        return True

    def atacar(self, alvo):

        return (
            self.estar_vivo()
            and alvo.receber_dano(self.dano)
        )

    def atualizar_efeito(self, dt):

        if self.tempo_efeito_dano > 0:

            self.tempo_efeito_dano -= dt

            if self.tempo_efeito_dano <= 0:

                self.imagem_atual = (
                    self.imagem_original.copy()
                )

    def sincronizar_hitbox(self):

        self.hitbox.center = (
            round(self.posicao.x),
            round(self.posicao.y)
        )

    def mover(
        self, direcao, dt,
        cenario, velocidade=None
    ):

        if not self.estar_vivo():
            return

        direcao = pygame.Vector2(direcao)

        if direcao.length_squared() == 0:
            return

        direcao = direcao.normalize()

        velocidade_real = (
            self.velocidade
            if velocidade is None
            else velocidade
        )

        passo = direcao * velocidade_real * dt

        # Movimento separado nos eixos X e Y
        for eixo in ("x", "y"):

            anterior = getattr(
                self.posicao, eixo
            )

            novo_valor = (
                anterior + getattr(passo, eixo)
            )

            setattr(
                self.posicao,
                eixo,
                novo_valor
            )

            self.sincronizar_hitbox()

            # Não atravessa terreno sólido
            if cenario.colide_solido(self.hitbox):

                setattr(
                    self.posicao,
                    eixo,
                    anterior
                )

                self.sincronizar_hitbox()

    def atualizar_visual(self, arma=None):
        

        base = pygame.Surface(
            (104, 104),
            pygame.SRCALPHA
        )

        
        base.blit(
            self.imagem_atual,
            (
                52 - self.tamanho // 2,
                52 - self.tamanho // 2
            )
        )

        
        if arma is not None:

            base.blit(
                arma.sprite,
                (
                    50,
                    52 - arma.sprite.get_height() // 2
                )
            )

        
        self.image = pygame.transform.rotate(
            base,
            self.angulo
        )

        self.rect = self.image.get_rect(
            center=self.hitbox.center
        )

    def update(self, dt, *args):
        self.atualizar(dt, *args)

    @abstractmethod
    def atualizar(self, dt, *args):
        pass


class Jogador(Boneco):

    def __init__(
        self, nome, x, y,
        velocidade=250, tamanho=40
    ):
        super().__init__(
            nome, x, y,
            vida=100,
            armadura=2,
            dano=10,
            velocidade=velocidade,
            tamanho=tamanho
        )

        
        self.arsenal = [
            MP5(),
            M8A1(),
            Balista(),
            LSAT(),
            RM870(),
            FiveSeven()
        ]

        self.indice_arma = 0
        self.invulneravel = 0.0
        self.dinheiro = 5

        self.atualizar_visual(
            self.arma_equipada
        )

    @property
    def arma_equipada(self):

        return self.arsenal[
            self.indice_arma
        ]

    def selecionar_arma(self, numero):

        if 1 <= numero <= len(self.arsenal):

            self.indice_arma = numero - 1

            self.atualizar_visual(
                self.arma_equipada
            )

            return True

        return False

    def receber_dano(self, quantidade):

       
        if self.invulneravel > 0:
            return False

        atingido = super().receber_dano(
            quantidade
        )

        if atingido:
            self.invulneravel = 0.8

        return atingido

    def mover_jogador(
        self, direcao, dt, cenario
    ):

       
        velocidade_real = (
            self.velocidade
            * max(
                0.65,
                1 - self.arma_equipada.peso * 0.04
            )
        )

        self.mover(
            direcao,
            dt,
            cenario,
            velocidade_real
        )

    def mirar(self, destino):

        direcao = (
            pygame.Vector2(destino)
            - self.posicao
        )

        if direcao.length_squared() > 0:

            self.angulo = math.degrees(
                math.atan2(
                    -direcao.y,
                    direcao.x
                )
            )

    def disparar(self, destino):

        direcao = (
            pygame.Vector2(destino)
            - self.posicao
        )

        return self.arma_equipada.atirar(
            self.posicao,
            direcao
        )

    def atualizar(self, dt):

        self.invulneravel = max(
            0.0,
            self.invulneravel - dt
        )

        self.atualizar_efeito(dt)

        
        for arma in self.arsenal:
            arma.atualizar(dt)

        self.atualizar_visual(
            self.arma_equipada
        )


class Npc(Boneco):

    def atualizar(self, dt):

        self.atualizar_efeito(dt)
        self.atualizar_visual()


class Inimigo(Boneco):

    def __init__(
        self, nome, x, y,
        vida=50, armadura=2, dano=10,
        velocidade=100, raio_visao=700,
        cor_base=(90, 150, 80)
    ):
        super().__init__(
            nome, x, y,
            vida, armadura, dano,
            velocidade, cor_base
        )

        self.raio_visao = raio_visao

        self.direcao = pygame.Vector2(1, 0)

        self.tempo_mudar_direcao = 0.0

        self.sortear_direcao()

    def gerar_sprite_pixelarray(self):

        self.imagem_original.fill(
            (0, 0, 0, 0)
        )

        t = self.tamanho

        with pygame.PixelArray(
            self.imagem_original
        ) as p:

            # Corpo
            p[7:19, 6:t-6] = (70, 50, 40)

            # Braços
            p[17:32, 7:12] = self.cor_base
            p[17:32, t-12:t-7] = self.cor_base

            # Mãos
            p[29:32, 7:12] = (180, 30, 30)
            p[29:32, t-12:t-7] = (180, 30, 30)

            # Cabeça
            p[9:24, 10:t-10] = self.cor_base

            # Olhos
            p[19:22, 12:15] = (240, 240, 240)
            p[19:22, t-15:t-12] = (240, 240, 240)

    def sortear_direcao(self):

        angulo = random.uniform(
            0,
            math.tau
        )

        self.direcao = pygame.Vector2(
            math.cos(angulo),
            math.sin(angulo)
        )

        self.tempo_mudar_direcao = (
            random.uniform(1, 3)
        )

    def atualizar(
        self, dt, jogador, cenario
    ):

        if not self.estar_vivo():
            return

        self.atualizar_efeito(dt)

        distancia = (
            jogador.posicao
            - self.posicao
        )

        if (
            jogador.estar_vivo()
            and 0 < distancia.length()
            <= self.raio_visao
        ):

            self.direcao = distancia.normalize()

        else:

            self.tempo_mudar_direcao -= dt

            if self.tempo_mudar_direcao <= 0:
                self.sortear_direcao()

        self.mover(
            self.direcao,
            dt,
            cenario
        )

        self.angulo = math.degrees(
            math.atan2(
                -self.direcao.y,
                self.direcao.x
            )
        )

        self.atualizar_visual()


class Zombie(Inimigo):

    def __init__(self, position):

        super().__init__(
            "Zumbi",
            position[0],
            position[1],
            vida=100,
            armadura=0,
            dano=10,
            velocidade=random.randint(60, 100),
            raio_visao=950,
            cor_base=random.choice([
                (90, 150, 80),
                (70, 120, 90),
                (120, 90, 140)
            ])
        )
