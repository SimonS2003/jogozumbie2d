
import pygame
import random

from personagens import Inimigo


class Zombie(pygame.sprite.Sprite, Inimigo):

    def __init__(self, position):

        pygame.sprite.Sprite.__init__(self)

        Inimigo.__init__(
            self,
            nome="Zumbi",
            x=position[0],
            y=position[1],  
            vida=100,
            armadura=0,
            dano=10,
            velocidade=random.randint(60, 100)
        )

        self.image = pygame.Surface((35, 35))
        self.image.fill((200, 40, 40))

        self.rect = self.image.get_rect(
            center=(round(self.x), round(self.y))
            )

        self.position = pygame.Vector2(self.x, self.y)

        self.health = self.vida

    def update(self, dt, player_position):

        direction = pygame.Vector2(player_position) - self.position

        if direction.length() > 0:

            direction = direction.normalize()
            self.position += direction * self.velocidade * dt

            self.x = self.position.x
            self.y = self.position.y

            self.rect.center = (
                round(self.position.x),
                round(self.position.y)
            )