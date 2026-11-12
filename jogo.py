
import math
import pygame
import random

from settings import *
from menu import Menu
from personagens import Jogador, Zombie
from entities.bullet import Bullet

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()
font = pygame.font.Font(None, 35)
pause_font = pygame.font.Font(None, 65)


MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"

game_state = MENU
running = True

pause_started = 0


menu = Menu(screen)

resume_button = pygame.Rect(WIDTH // 2 - 120,HEIGHT // 2 - 10,240,55)

menu_button = pygame.Rect(WIDTH // 2 - 120,HEIGHT // 2 + 65,240,55)



player = Jogador(
    nome="Sobrevivente",
    x=WIDTH // 2,
    y=HEIGHT // 2,
    dano=25,
    velocidade=PLAYER_SPEED,
    tamanho=PLAYER_SIZE
)



bullets = pygame.sprite.Group()
zombies = pygame.sprite.Group()



shoot_cooldown = 250
last_shot = 0

spawn_interval = 1500
last_spawn = 0

damage_cooldown = 600 # Tempo de invencibilidade entre mordidas de zumbi (ms)

last_player_hit = 0



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



def resume_game():

    global game_state
    global last_spawn
    global last_shot
    global last_player_hit

    pause_duration = pygame.time.get_ticks() - pause_started

    last_spawn += pause_duration
    last_shot += pause_duration
    last_player_hit += pause_duration

    game_state = PLAYING



while running:

    dt = clock.tick(FPS) / 1000.0

    current_time = pygame.time.get_ticks()



    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif game_state == MENU:

            action = menu.handle_event(event)

            if action == "play":

                game_state = PLAYING

                player.x = float(WIDTH // 2)
                player.y = float(HEIGHT // 2)

                player.vida = player.vida_maxima

                player.atualizar(0, screen.get_rect())

                bullets.empty()
                zombies.empty()

                score = 0

                current_time = pygame.time.get_ticks()

                last_spawn = current_time
                last_shot = current_time
                last_player_hit = current_time


            elif action == "quit":

                running = False

        elif game_state == PLAYING:

            if event.type == pygame.KEYDOWN:

                # PAUSAR COM ESC
                if event.key == pygame.K_ESCAPE:

                    game_state = PAUSED

                    pause_started = pygame.time.get_ticks()


                # Aperte 'C' durante o jogo para mudar a cor da roupa do jogador 
                elif event.key == pygame.K_c:

                    nova_cor = (random.randint(50, 255), random.randint(50, 255),random.randint(50, 255))
                    player.trocar_cor(player.cor_base,nova_cor)

        
        elif game_state == PAUSED:

            if event.type == pygame.KEYDOWN:

                # ESC PARA CONTINUAR
                if event.key == pygame.K_ESCAPE:

                    resume_game()


            # CLIQUES NOS BOTÕES
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    mouse_pos = event.pos

                    # CONTINUAR
                    if resume_button.collidepoint(mouse_pos):

                        resume_game()


                    # VOLTAR AO MENU
                    elif menu_button.collidepoint(mouse_pos):

                        game_state = MENU



    if game_state == PLAYING:


        keys = pygame.key.get_pressed()

        dir_x = float(keys[pygame.K_d] - keys[pygame.K_a])

        dir_y = float(keys[pygame.K_s] - keys[pygame.K_w])

        player.movimentacao(dir_x, dir_y, dt)

        player.atualizar(dt, screen.get_rect())

        player_position = pygame.Vector2(player.x,player.y)


        mouse_buttons = pygame.mouse.get_pressed()

        if (mouse_buttons[0] and current_time - last_shot >= shoot_cooldown):

            mouse_position = pygame.Vector2(pygame.mouse.get_pos())

            shoot_direction = mouse_position - player_position

            if shoot_direction.length() > 0:

                shoot_direction = shoot_direction.normalize()

                bullet = Bullet(player.rect.center,shoot_direction)

                bullets.add(bullet)

                last_shot = current_time


        bullets.update(dt)

        # 3. Spawn e Atualização dos Zumbis (passando o objeto 'player' como alvo!)

        if current_time - last_spawn >= spawn_interval:

            spawn_zombie()

            last_spawn = current_time



        zombies.update(dt, player)

         # 4. Colisão entre Tiros e Zumbis (usa receber_dano e estar_vivo de Boneco)

        for zombie in zombies:

            hits = pygame.sprite.spritecollide(zombie,bullets,True)

            for bullet in hits:

                zombie.receber_dano(bullet.damage)

                if not zombie.estar_vivo():

                    zombie.kill()

                    score += 1

        # 5. Colisão entre Zumbis e Jogador (Zumbi ataca o Jogador!)
        if current_time - last_player_hit >= damage_cooldown:

            for zombie in zombies:

                if player.rect.colliderect(zombie.rect):

                    zombie.atacar(player)

                    last_player_hit = current_time

                    if not player.estar_vivo():

                        game_state = MENU

                    break


                # Desenhando elementos na tela
    if game_state == MENU:

        menu.draw()



    elif game_state == PLAYING or game_state == PAUSED:

        screen.fill((45, 45, 45))


         # Calcula direção do mouse para girar o sprite do Jogador (Bird View)

        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

        aim_dir = mouse_pos - pygame.Vector2(player.x, player.y)

        player.desenhar(screen,aim_dir.x,aim_dir.y)



        bullets.draw(screen)

        zombies.draw(screen)

        # HUD: Placar e Vida do Jogador
        score_text = font.render(
            f"Zumbis eliminados: {score} | Vida: {player.vida}/{player.vida_maxima}",True,WHITE)

        screen.blit(score_text, (20, 20))


        controls = font.render(
            "WASD: Mover | Mouse: Atirar | C: Cor | ESC: Pausar",True,WHITE)

        screen.blit(controls,(20, HEIGHT - 40))

        #Quando o jogo estiver pausado, desenha a tela de pausa com opções de continuar ou voltar ao menu
        if game_state == PAUSED:

            overlay = pygame.Surface((WIDTH, HEIGHT),pygame.SRCALPHA)

            overlay.fill((0, 0, 0, 190))

            screen.blit(overlay, (0, 0))

            pause_title = pause_font.render("JOGO PAUSADO",True,WHITE)

            title_rect = pause_title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

            screen.blit(pause_title,title_rect)

            pygame.draw.rect(screen,(40, 150, 70),resume_button,border_radius=10)

            resume_text = font.render("CONTINUAR",True,WHITE)

            resume_rect = resume_text.get_rect(center=resume_button.center)

            screen.blit(resume_text,resume_rect)

            pygame.draw.rect(screen,(150, 50, 50),menu_button,border_radius=10)

            menu_text = font.render("VOLTAR AO MENU",True,WHITE)

            menu_rect = menu_text.get_rect(center=menu_button.center)

            screen.blit(menu_text,menu_rect)



    pygame.display.flip()



pygame.quit()
