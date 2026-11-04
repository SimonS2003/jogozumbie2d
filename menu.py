
import pygame

from settings import (
    WIDTH,
    HEIGHT,
    WHITE,
    BLACK,
    GREEN,
    GRAY,
    DARK_GRAY
)


class Menu:

    def __init__(self, screen):

        self.screen = screen

        self.title_font = pygame.font.Font(None, 90)
        self.button_font = pygame.font.Font(None, 45)

        self.play_button = pygame.Rect(
            WIDTH // 2 - 150,
            HEIGHT // 2 - 20,
            300,
            70
        )

        self.exit_button = pygame.Rect(
            WIDTH // 2 - 150,
            HEIGHT // 2 + 90,
            300,
            70
        )

    def draw(self):

        self.screen.fill(BLACK)

        # Título
        title = self.title_font.render(
            "ZOMBIE SURVIVAL",
            True,
            GREEN
        )

        title_rect = title.get_rect(
            center=(WIDTH // 2, HEIGHT // 3)
        )

        self.screen.blit(title, title_rect)

        # Botão jogar
        pygame.draw.rect(
            self.screen,
            GREEN,
            self.play_button,
            border_radius=10
        )

        play_text = self.button_font.render(
            "JOGAR",
            True,
            BLACK
        )

        play_rect = play_text.get_rect(
            center=self.play_button.center
        )

        self.screen.blit(play_text, play_rect)

        # Botão sair
        pygame.draw.rect(
            self.screen,
            GRAY,
            self.exit_button,
            border_radius=10
        )

        exit_text = self.button_font.render(
            "SAIR",
            True,
            WHITE
        )

        exit_rect = exit_text.get_rect(
            center=self.exit_button.center
        )

        self.screen.blit(exit_text, exit_rect)

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                if self.play_button.collidepoint(event.pos):
                    return "play"

                if self.exit_button.collidepoint(event.pos):
                    return "quit"

        return None
