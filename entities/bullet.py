
import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, position, direction):

        super().__init__()

        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)

        pygame.draw.circle(
            self.image,
            (255, 220, 50),
            (5, 5),
            5
        )

        self.rect = self.image.get_rect(center=position)

        self.position = pygame.Vector2(position)
        self.direction = pygame.Vector2(direction)

        self.speed = 600
        self.damage = 50

    def update(self, dt):

        self.position += self.direction * self.speed * dt

        self.rect.center = (
            round(self.position.x),
            round(self.position.y)
        )

        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()
