import math
import pygame
import random

from settings import *
from menu import Menu

from entities.bullet import Bullet
from entities.zombie import Zombie


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()

font = pygame.font.Font(None, 35)

MENU = "menu"
PLAYING = "playing"

game_state = MENU
running = True

menu = Menu(screen)

player = pygame.Rect(
    WIDTH // 2 - PLAYER_SIZE // 2,
    HEIGHT // 2 - PLAYER_SIZE // 2,
    PLAYER_SIZE,
    PLAYER_SIZE
)

player_position = pygame.Vector2(player.center)

def criar_sprite_jogador(tamanho, cor_roupa=(0, 140, 255)):
    surf = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
    with pygame.PixelArray(surf) as pixels:
        # Ombros / Corpo
        pixels[6:18, 4:tamanho-4] = cor_roupa
        # Braços esticados segurando a arma para a frente (direita)
        pixels[16:26, 8:12] = (230, 190, 150)
        pixels[16:26, tamanho-12:tamanho-8] = (230, 190, 150)
        # Arma apontando para a direita
        pixels[20:tamanho, tamanho//2 - 2 : tamanho//2 + 2] = (40, 40, 40)
        # Cabeça vista de cima e boné/capacete
        pixels[8:20, 8:tamanho-8] = (240, 200, 160)
        pixels[7:14, 8:tamanho-8] = (20, 60, 130)
    return surf

player_base_image = criar_sprite_jogador(PLAYER_SIZE)

bullets = pygame.sprite.Group()
zombies = pygame.sprite.Group()


shoot_cooldown = 250
last_shot = 0

spawn_interval = 1500
last_spawn = 0

score = 0


def spawn_zombie():

    side = random.randint(0, 3)

    if side == 0:
        position = (random.randint(0, WIDTH), -40)

    elif side == 1:
        position = (random.randint(0, WIDTH), HEIGHT + 40)

    elif side == 2:
        position = (-40, random.randint(0, HEIGHT))

    else:
        position = (WIDTH + 40, random.randint(0, HEIGHT))

    zombie = Zombie(position)

    zombies.add(zombie)


while running:

    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if game_state == MENU:

            action = menu.handle_event(event)

            if action == "play":

                game_state = PLAYING

                player.center = (WIDTH // 2, HEIGHT // 2)
                player_position = pygame.Vector2(player.center)

                bullets.empty()
                zombies.empty()

                score = 0

                last_spawn = pygame.time.get_ticks()

            elif action == "quit":
                running = False

        elif game_state == PLAYING:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    game_state = MENU

                # Aperte 'C' durante o jogo para mudar a cor da roupa do jogador 
                elif event.key == pygame.K_c:
                    nova_cor = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                    player_base_image = criar_sprite_jogador(PLAYER_SIZE, nova_cor)
#teclas de movimentação do jogadors
    if game_state == PLAYING:

        keys = pygame.key.get_pressed()

        direction = pygame.Vector2(0, 0)

        if keys[pygame.K_w]:
            direction.y -= 1

        if keys[pygame.K_s]:
            direction.y += 1

        if keys[pygame.K_a]:
            direction.x -= 1

        if keys[pygame.K_d]:
            direction.x += 1

        if direction.length() > 0:
            direction = direction.normalize()

        player_position += direction * PLAYER_SPEED * dt
        player.center = (
            round(player_position.x),
            round(player_position.y)
        )
        player.clamp_ip(screen.get_rect())
        player_position = pygame.Vector2(player.center)

#Disparo de tiros
        mouse_buttons = pygame.mouse.get_pressed()

        current_time = pygame.time.get_ticks()

        if mouse_buttons[0]:

            if current_time - last_shot >= shoot_cooldown:

                mouse_position = pygame.Vector2(
                    pygame.mouse.get_pos()
                )

                shoot_direction = mouse_position - player_position

                if shoot_direction.length() > 0:

                    shoot_direction = shoot_direction.normalize()

                    bullet = Bullet(
                        player.center,
                        shoot_direction
                    )

                    bullets.add(bullet)

                    last_shot = current_time

# Atualizar tiros
        bullets.update(dt)


# Spawn de zumbies
        if current_time - last_spawn >= spawn_interval:

            spawn_zombie()

            last_spawn = current_time


        # Zumbis perseguem jogadorwa
        zombies.update(dt, player_position)


#Colisão entre zumbis e tiros
        for zombie in zombies:

            hits = pygame.sprite.spritecollide(
                zombie,
                bullets,
                True
            )

            for bullet in hits:

                zombie.receber_dano(bullet.damage)

                if not zombie.estar_vivo():
                    zombie.kill()
                    score += 1

#Desenhando elementos na tela
    if game_state == MENU:

        menu.draw()

    elif game_state == PLAYING:

        screen.fill((45, 45, 45))

        # desenhando o jogador
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        aim_dir = mouse_pos - player_position
        angulo_player = math.degrees(math.atan2(-aim_dir.y, aim_dir.x)) if aim_dir.length() > 0 else 0

        player_rotated = pygame.transform.rotate(player_base_image, angulo_player)
        player_rect_draw = player_rotated.get_rect(center=player.center)
        screen.blit(player_rotated, player_rect_draw.topleft)

        # Desenhando os tiros
        bullets.draw(screen)

        # Desenhando os  zumbis
        zombies.draw(screen)

        # HUD
        score_text = font.render(
            f"Zumbis eliminados: {score}",
            True,
            WHITE
        )

        screen.blit(score_text, (20, 20))

        controls = font.render(
            "WASD: Mover | Mouse: Atirar | ESC: Menu",
            True,
            WHITE
        )

        screen.blit(
            controls,
            (20, HEIGHT - 40)
        )


    pygame.display.flip()


pygame.quit()
