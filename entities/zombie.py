
import pygame
import random
import math
from personagens import Inimigo


class Zombie(pygame.sprite.Sprite, Inimigo):

    def __init__(self, position):

        pygame.sprite.Sprite.__init__(self)

        cor_zumbi = random.choice([
            (90, 150, 80), 
            (70, 120, 90), 
            (120, 90, 140)
            ])

        Inimigo.__init__(
            self,
            nome="Zumbi",
            x=position[0],
            y=position[1],  
            vida=100,
            armadura=0,
            dano=10,
            velocidade=random.randint(60, 100),
            raio_visao=1350.0,
            cor_base=cor_zumbi
        )

        self.image = self.imagem_atual
        self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))
        self.position = pygame.Vector2(self.x, self.y)


    def update(self, dt, alvo):

        self.atualizar(dt, alvo)

        self.position.x = self.x
        self.position.y = self.y

        # 3. Gira a imagem do PixelArray na direção em que o zumbi está andando (Bird View)
        angulo = math.degrees(math.atan2(-self.direcao_y, self.direcao_x))
        self.image = pygame.transform.rotate(self.imagem_atual, angulo)
        self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))