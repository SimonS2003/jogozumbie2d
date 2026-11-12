import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(
        self, position, direction,
        dano, velocidade, alcance
    ):
        super().__init__()

        self.image = pygame.Surface(
            (8, 8), pygame.SRCALPHA
        )

        pygame.draw.circle(
            self.image,
            (255, 215, 65),
            (4, 4),
            4
        )

        self.posicao = pygame.Vector2(position)

        self.direcao = pygame.Vector2(
            direction
        ).normalize()

        self.velocidade = velocidade
        self.dano = dano
        self.alcance = alcance

        self.distancia = 0.0

        self.rect = self.image.get_rect(
            center=self.posicao
        )

    def update(self, dt, cenario):

        deslocamento = (
            self.direcao
            * self.velocidade
            * dt
        )

        self.posicao += deslocamento
        self.distancia += deslocamento.length()

        self.rect.center = (
            round(self.posicao.x),
            round(self.posicao.y)
        )

        
        if (
            self.distancia >= self.alcance
            or cenario.colide_solido(self.rect)
        ):
            self.kill()
