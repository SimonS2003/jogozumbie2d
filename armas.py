from abc import ABC, abstractmethod 
import random
import pygame
from entities.bullet import Bullet

class Arma(ABC):
    def __init__(self, nome, dano, pente, reserva, recarga,
        cadencia, velocidade_bala, alcance, peso,
        cor, comprimento, automatico=False,
        projeteis=1, dispersao=0, preco=0):
        
        self.nome = nome
        self.dano = dano

        self.capacidade_pente = pente
        self.municao_no_pente = pente
        self.municao_reserva = reserva

        self.tempo_recarga = recarga
        self.cadencia = cadencia
        self.velocidade_bala = velocidade_bala
        self.alcance = alcance
        self.peso = peso

        self.automatico = automatico
        self.tipo_disparo = ("Automático" if automatico
            else "Semiautomático")
        self.projeteis = projeteis
        self.dispersao = dispersao
        self.preco = preco

        self.recarregando = False
        self.tempo_restante = 0.0
        self.cooldown = 0.0

        self.sprite = self.criar_sprite_pixelarray(cor, comprimento)

    @staticmethod
    def criar_sprite_pixelarray(cor, comprimento):
        

        superficie = pygame.Surface(
            (comprimento, 16),
            pygame.SRCALPHA
        )

        with pygame.PixelArray(superficie) as p:

           
            p[1:comprimento-1, 7:10] = (31, 36, 39)

            
            p[4:min(22, comprimento-4), 5:11] = cor

            
            p[8:13, 10:15] = (100, 70, 42)

            
            p[comprimento-4:comprimento-1, 6:11] = (
                18, 22, 23
            )

            
            p[2:7, 6:9] = (78, 82, 83)

        return superficie




    def atualizar(self, dt):
        self.cooldown = max(
            0.0,
            self.cooldown - dt
        )

        if self.recarregando:

            self.tempo_restante -= dt

            if self.tempo_restante <= 0:

                quantidade = min(
                    self.capacidade_pente
                    - self.municao_no_pente,
                    self.municao_reserva
                )

                self.municao_no_pente += quantidade
                self.municao_reserva -= quantidade

                self.recarregando = False
                self.tempo_restante = 0.0

    def iniciar_recarga(self):

        if (
            self.recarregando
            or self.municao_reserva <= 0
            or self.municao_no_pente
               == self.capacidade_pente
        ):
            return False

        self.recarregando = True
        self.tempo_restante = self.tempo_recarga

        return True

    def atirar(self, origem, direcao):

        if (
            self.recarregando
            or self.cooldown > 0
            or self.municao_no_pente <= 0
        ):
            return []

        direcao = pygame.Vector2(direcao)

        if direcao.length_squared() == 0:
            return []

        direcao = direcao.normalize()

        self.municao_no_pente -= 1
        self.cooldown = 1.0 / self.cadencia

        # Bala sai à frente do personagem
        saida = pygame.Vector2(origem) + direcao * 26

        balas = []

        for _ in range(self.projeteis):

            desvio = random.uniform(
                -self.dispersao,
                self.dispersao
            )

            nova_direcao = direcao.rotate(desvio)

            bala = Bullet(
                saida,
                nova_direcao,
                dano=self.dano,
                velocidade=self.velocidade_bala,
                alcance=self.alcance
            )

            balas.append(bala)

        return balas



class Submetralhadora(Arma):
    pass


class FuzilDeAssalto(Arma):
    pass


class FuzilDePrecisao(Arma):
    pass


class MetralhadoraLeve(Arma):
    pass


class Escopeta(Arma):
    pass


class Pistola(Arma):
    pass



class MP5(Submetralhadora):

    def __init__(self):
        super().__init__(
            "MP5", 20, 30, 120, 2.0,
            6, 700, 750, 2,
            (62, 92, 110), 34,
            automatico=True
        )


class M8A1(FuzilDeAssalto):

    def __init__(self):
        super().__init__(
            "M8A1", 36, 45, 135, 2.5,
            4, 800, 850, 3,
            (77, 116, 66), 41
        )


class Balista(FuzilDePrecisao):

    def __init__(self):
        super().__init__(
            "Balista", 95, 8, 32, 3.5,
            1.2, 1050, 1200, 4,
            (105, 78, 53), 46
        )


class LSAT(MetralhadoraLeve):

    def __init__(self):
        super().__init__(
            "LSAT", 25, 60, 180, 4.5,
            8, 760, 850, 6,
            (104, 95, 66), 44,
            automatico=True
        )


class RM870(Escopeta):

    def __init__(self):
        super().__init__(
            "RM870", 13, 8, 40, 3.0,
            1.1, 570, 370, 5,
            (115, 70, 40), 40,
            projeteis=6,
            dispersao=14
        )


class FiveSeven(Pistola):

    def __init__(self):
        super().__init__(
            "Five-Seven", 26, 15, 75, 1.5,
            3.5, 760, 650, 1,
            (85, 85, 96), 23
        )