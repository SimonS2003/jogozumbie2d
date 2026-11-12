import math
import random
import pygame


class Cenario:
    

    def __init__(
        self, colunas=80,
        linhas=60, tile=40
    ):
        self.colunas = colunas
        self.linhas = linhas
        self.tile = tile

        self.largura = colunas * tile
        self.altura = linhas * tile

        self.limites = pygame.Rect(
            0, 0,
            self.largura,
            self.altura
        )

       
        self.solidos = {"agua", "pedra"}

        rng = random.Random(42)

        self.texturas = {}

        
        tipos = [
            ("grama", (62, 126, 50), (91, 155, 57)),
            ("grama2", (53, 115, 49), (78, 139, 47)),
            ("terra", (145, 110, 73), (172, 137, 91)),
            ("agua", (36, 125, 185), (89, 180, 214)),
            ("pedra", (79, 88, 81), (110, 115, 103)),
            ("ponte", (125, 85, 47), (166, 110, 65))
        ]

        
        for nome, cor, pontos in tipos:

            superficie = pygame.Surface(
                (tile, tile)
            ).convert()

            with pygame.PixelArray(superficie) as p:

                p[:, :] = cor

                for _ in range(95):

                    x = rng.randrange(tile)
                    y = rng.randrange(tile)

                    p[x, y] = pontos

            self.texturas[nome] = superficie

        
        self.mapa = []

        for y in range(linhas):

            linha = []

            rio = 62 + round(
                2 * math.sin(y / 5)
            )

            for x in range(colunas):

                if abs(x - rio) <= 2:
                    tipo = (
                        "ponte"
                        if 18 <= y <= 20
                        else "agua"
                    )

                elif (
                    10 <= x <= 14
                    and 8 <= y <= 13
                ):
                    tipo = "pedra"

                elif (
                    34 <= x <= 47
                    and 25 <= y <= 35
                ):
                    tipo = "terra"

                else:
                    tipo = (
                        "grama2"
                        if rng.random() < 0.25
                        else "grama"
                    )

                linha.append(tipo)

            self.mapa.append(linha)

    def colide_solido(self, rect):

        
        if not self.limites.contains(rect):
            return True

        t = self.tile

        
        for y in range(
            rect.top // t,
            (rect.bottom - 1) // t + 1
        ):

            for x in range(
                rect.left // t,
                (rect.right - 1) // t + 1
            ):

                tipo = self.mapa[y][x]

                if tipo in self.solidos:
                    return True

        return False

    def desenhar(self, tela, camera):

        t = self.tile

        
        x0 = max(0, int(camera.x // t))
        y0 = max(0, int(camera.y // t))

        x1 = min(
            self.colunas,
            int(
                (camera.x + tela.get_width()) // t
            ) + 2
        )

        y1 = min(
            self.linhas,
            int(
                (camera.y + tela.get_height()) // t
            ) + 2
        )

        
        for y in range(y0, y1):

            for x in range(x0, x1):

                tipo = self.mapa[y][x]
                imagem = self.texturas[tipo]

                tela.blit(
                    imagem,
                    (
                        round(x * t - camera.x),
                        round(y * t - camera.y)
                    )
                )


class Camera:

    def __init__(self, cenario, tamanho_tela):

        self.cenario = cenario

        self.largura, self.altura = tamanho_tela

        self.x = 0.0
        self.y = 0.0

    def seguir(self, posicao, dt, imediato=False):

        
        lim_x = max(
            0,
            self.cenario.largura - self.largura
        )

        lim_y = max(
            0,
            self.cenario.altura - self.altura
        )

        
        dest_x = max(
            0,
            min(
                posicao.x - self.largura / 2,
                lim_x
            )
        )

        dest_y = max(
            0,
            min(
                posicao.y - self.altura / 2,
                lim_y
            )
        )

        
        fator = (
            1.0
            if imediato
            else min(1.0, dt * 8)
        )

        self.x += (dest_x - self.x) * fator
        self.y += (dest_y - self.y) * fator

    def aplicar(self, rect):
        

        return rect.move(
            -round(self.x),
            -round(self.y)
        )

    def tela_para_mundo(self, ponto):
        

        return (
            pygame.Vector2(ponto)
            + pygame.Vector2(self.x, self.y)
        )