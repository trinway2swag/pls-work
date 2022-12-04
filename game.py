import pygame
import cocolady
import gringo
import fatjoe
import sprites
import random

# initialize pygame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# create a game display
pygame.display.set_icon(sprites.icon)
display_width = 800
display_height = 600
game_display = pygame.display.set_mode((display_width, display_height))

# 8 bit madness font can be downloaded from here: http://www.dafont.com/8-bit-madness.font
font = "8-Bit-Madness.ttf"


# text rendering function
def message_to_screen(message, textfont, size, color):
    my_font = pygame.font.Font(textfont, size)
    my_message = my_font.render(message, 0, color)

    return my_message

# colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# sprite pixel format converting
for convert_sprites in sprites.all_sprites:
    convert_sprites.convert_alpha()

# framerate
clock = pygame.time.Clock()
FPS = 30

# player variables
player = cocolady.Cocolady(100, display_height/2-40)
moving = True
godmode = False

# score variables
score = 0
highscore_file = open('highscore.dat', "r")
highscore_int = int(highscore_file.read())

# cloud variables
cloud_x = 800
cloud_y = random.randint(0, 400)

# gringo variables
gringo = gringo.Gringo(-100, display_height/2-40)
gringo_alive = False

# FatJoe variables
fatjoe = fatjoe.FatJoe(-110, 430)
fatjoe_alive = False

# karen variables
karen_x = 800
karen_y = random.randint(0, 400)
karen_alive = False
karen_hit_player = False
warning_once = True
warning = False
warning_counter = 0
warning_message = message_to_screen("!", font, 200, red)

# crab variables
crab_x = 800
crab= random.randint(0, 400)

# bullet variables
bullets = []

# bomb variables
bombs = []

# sounds
pop = pygame.mixer.Sound('sounds/pop.wav')
shoot = pygame.mixer.Sound('sounds/shoot.wav')
bomb = pygame.mixer.Sound('sounds/bomb.wav')
explosion = pygame.mixer.Sound('sounds/explosion.wav')
explosion2 = pygame.mixer.Sound('sounds/explosion2.wav')
select = pygame.mixer.Sound('sounds/select.wav')
select2 = pygame.mixer.Sound('sounds/select2.wav')
alert = pygame.mixer.Sound('sounds/alert.wav')
whoosh = pygame.mixer.Sound('sounds/whoosh.wav')


# main menu
def main_menu():

    global cloud_x
    global cloud_y

    menu = True

    selected = "play"

    while menu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(select)
                    selected = "play"
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    pygame.mixer.Sound.play(select)
                    selected = "quit"
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.play(select2)
                    if selected == "play":
                        menu = False
                    if selected == "quit":
                        pygame.quit()
                        quit()

        # drawing background
        game_display.blit(sprites.background, (0, 0))

        game_display.blit(sprites.cloud, (cloud_x, cloud_y))
        if cloud_x <= 800 - 1100:
            cloud_x = 800
            cloud_y = random.randint(0, 400)
        else:
            if not player.wreck_start:
                cloud_x -= 5
        if godmode:
            title = message_to_screen("COCOLADY (GODMODE)", font, 80, yellow)
        else:
            title = message_to_screen("COCOLADY", font, 100, black)
        controls_1 = message_to_screen("use WASD to move, SPACE to shoot,", font, 30, black)
        controls_2 = message_to_screen("SHIFT to drop bombs, and P to toggle pause", font, 30, black)
        if selected == "play":
            play = message_to_screen("PLAY", font, 75, white)
        else:
            play = message_to_screen("PLAY", font, 75, black)
        if selected == "quit":
            game_quit = message_to_screen("QUIT", font, 75, white)
        else:
            game_quit = message_to_screen("QUIT", font, 75, black)

        title_rect = title.get_rect()
        controls_1_rect = controls_1.get_rect()
        controls_2_rect = controls_2.get_rect()
        play_rect = play.get_rect()
        quit_rect = game_quit.get_rect()

        # drawing text
        game_display.blit(title, (display_width/2 - (title_rect[2]/2), 40))
        game_display.blit(controls_1, (display_width/2 - (controls_1_rect[2]/2), 120))
        game_display.blit(controls_2, (display_width/2 - (controls_2_rect[2]/2), 140))
        game_display.blit(play, (display_width/2 - (play_rect[2]/2), 200))
        game_display.blit(game_quit, (display_width/2 - (quit_rect[2]/2), 260))
        # drawing ocean
        pygame.draw.rect(game_display, blue, (0, 500, 800, 100))

        pygame.display.update()
        pygame.display.set_caption("COCOLADY running at " + str(int(clock.get_fps())) + " frames per second.")
        clock.tick(FPS)


def pause():

    global highscore_file
    global highscore_int

    paused = True

    player.moving_up = False
    player.moving_left = False
    player.moving_down = False
    player.moving_right = False

    paused_text = message_to_screen("PAUSED", font, 100, black)
    paused_text_rect = paused_text.get_rect()

    game_display.blit(paused_text, (display_width/2 - (paused_text_rect[2]/2), 40))

    pygame.display.update()
    clock.tick(15)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > highscore_int:
                    highscore_file = open('highscore.dat', "w")
                    highscore_file.write(str(score))
                    highscore_file.close()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.mixer.Sound.play(select)
                    paused = False


# create a game loop
def game_loop():

    global karen_x
    global karen_y
    global karen_alive
    global karen_hit_player
    global warning
    global warning_counter
    global warning_once

    global bullets
    global moving

    global highscore_file
    global highscore_int
    global score

    global cloud_x
    global cloud_y

    global crab_x
    global crab_y

    global gringo_alive

    global fatjoe_alive

    game_exit = False
    game_over = False

    game_over_selected = "play again"

    while not game_exit:

        while game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if score > highscore_int:
                        highscore_file = open('highscore.dat', "w")
                        highscore_file.write(str(score))
                        highscore_file.close()
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        pygame.mixer.Sound.play(select)
                        game_over_selected = "play again"
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        pygame.mixer.Sound.play(select)
                        game_over_selected = "quit"
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        pygame.mixer.Sound.play(select2)
                        if game_over_selected == "play again":
                            if score > highscore_int:
                                highscore_file = open('highscore.dat', "w")
                                highscore_file.write(str(score))
                                highscore_file.close()
                            game_over = False

                            score = 0

                            crab_x = 800

                            gringo.x = -100
                            gringo_alive = False
                            gringo.bullets = []

                            fatjoe.x = -110
                            fatjoe_alive = False
                            fatjoe.bullets = []

                            karen_x = 800
                            karen_alive = False
                            warning = False
                            warning_counter = 0
                            warning_counter = 0

                            player.wreck_start = False
                            player.y = display_height/2-40
                            player.x = 100
                            player.wrecked = False
                            player.health = 3
                            bullets = []

                            game_loop()
                        if game_over_selected == "quit":
                            pygame.quit()
                            quit()

            game_over_text = message_to_screen("GAME OVER", font, 100, black)
            your_score = message_to_screen("YOUR SCORE WAS: " + str(score), font, 50, black)
            if game_over_selected == "play again":
                play_again = message_to_screen("PLAY AGAIN", font, 75, white)
            else:
                play_again = message_to_screen("PLAY AGAIN", font, 75, black)
            if game_over_selected == "quit":
                game_quit = message_to_screen("QUIT", font, 75, white)
            else:
                game_quit = message_to_screen("QUIT", font, 75, black)

            game_over_rect = game_over_text.get_rect()
            your_score_rect = your_score.get_rect()
            play_again_rect = play_again.get_rect()
            game_quit_rect = game_quit.get_rect()

            game_display.blit(game_over_text, (display_width/2 - game_over_rect[2]/2, 40))
            game_display.blit(your_score, (display_width/2 - (your_score_rect[2]/2+5), 100))
            game_display.blit(play_again, (display_width/2 - play_again_rect[2]/2, 200))
            game_display.blit(game_quit, (display_width/2 - game_quit_rect[2]/2, 260))

            pygame.display.update()
            pygame.display.set_caption("COCOLADY running at " + str(int(clock.get_fps())) + " frames per second.")
            clock.tick(10)

        # event handler
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                if score > highscore_int:
                    highscore_file = open('highscore.dat', "w")
                    highscore_file.write(str(score))
                    highscore_file.close()
                pygame.quit()
                quit()

            if moving:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        player.moving_up = True
                    if event.key == pygame.K_a:
                        player.moving_left = True
                    if event.key == pygame.K_s:
                        player.moving_down = True
                    if event.key == pygame.K_d:
                        player.moving_right = True
                    if event.key == pygame.K_SPACE:
                        if not player.wreck_start:
                            pygame.mixer.Sound.play(shoot)
                            bullets.append([player.x, player.y])
                    if event.key == pygame.K_LSHIFT:
                        if not player.wreck_start:
                            pygame.mixer.Sound.play(bomb)
                            bombs.append([player.x, player.y])
                    if event.key == pygame.K_p:
                        pygame.mixer.Sound.play(select)
                        pause()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        player.moving_up = False
                    if event.key == pygame.K_a:
                        player.moving_left = False
                    if event.key == pygame.K_s:
                        player.moving_down = False
                    if event.key == pygame.K_d:
                        player.moving_right = False

        if player.health < 1:
            pygame.mixer.Sound.play(explosion)
            player.wreck()

        if player.wrecked:
            game_over = True

        # draw background and randomly positioned clouds
        game_display.blit(sprites.background, (0, 0))

        game_display.blit(sprites.cloud, (cloud_x, cloud_y))
        if cloud_x <= 800 - 1100:
            cloud_x = 800
            cloud_y = random.randint(0, 400)
        else:
            if not player.wreck_start:
                cloud_x -= 5

        # drawing player
        game_display.blit(player.current, (player.x, player.y))

        # drawing Gringo
        game_display.blit(gringo.current, (gringo.x, gringo.y))

        # drawing karen
        game_display.blit(sprites.karen, (karen_x, karen_y))

        # drawing fatjoe
        game_display.blit(sprites.fatjoe, (fatjoe.x, fatjoe.y))

        # enabling movement and animations
        player.player_init()
        gringo.init()
        fatjoe.init()

        # rendering bullets
        if not player.wreck_start and not player.wrecked:
            for draw_bullet in bullets:
                pygame.draw.rect(game_display, black, (draw_bullet[0]+90, draw_bullet[1]+40, 10, 10))
            for move_bullet in range(len(bullets)):
                bullets[move_bullet][0] += 40
            for del_bullet in bullets:
                if del_bullet[0] >= 800:
                    bullets.remove(del_bullet)

        # rendering bombs
        if not player.wreck_start and not player.wrecked:
            for draw_bomb in bombs:
                pygame.draw.rect(game_display, black, (draw_bomb[0]+55, draw_bomb[1]+70, 20, 20))
            for move_bomb in range(len(bombs)):
                bombs[move_bomb][1] += 20
            for del_bomb in bombs:
                if del_bomb[1] > 600:
                    bombs.remove(del_bomb)

        # rendering gringo bullets
        if not player.wreck_start and not player.wrecked and not game_over:
            for draw_bullet in gringo.bullets:
                pygame.draw.rect(game_display, gray, (draw_bullet[0], draw_bullet[1]+40, 40, 10))
                pygame.draw.rect(game_display, red, (draw_bullet[0]+30, draw_bullet[1]+40, 10, 10))
            for move_bullet in range(len(gringo.bullets)):
                gringo.bullets[move_bullet][0] -= 15
            for del_bullet in gringo.bullets:
                if del_bullet[0] <= -40:
                    gringo.bullets.remove(del_bullet)

        # rendering fatjoe bullets
        if not player.wreck_start and not player.wrecked and not game_over:
            for draw_bullet in fatjoe.bullets:
                pygame.draw.rect(game_display, gray, (draw_bullet[0]+40, draw_bullet[1]+30, 20, 20))
            for move_bullet in range(len(fatjoe.bullets)):
                fatjoe.bullets[move_bullet][0] -= 10
                fatjoe.bullets[move_bullet][1] -= 10
            for del_bullet in fatjoe.bullets:
                if del_bullet[1] < -40:
                    fatjoe.bullets.remove(del_bullet)

        # draw randomly positioned crabs, pop if they hit any bullet or bombs
        for pop_crab in bullets:
            if crab_x < pop_crab[0]+90 < crab_x+70 and crab_y < pop_crab[1]+40 < crab_y+100:
                pygame.mixer.Sound.play(pop)
                bullets.remove(pop_crab)
                crab_x = 800-870
                score += 50
            elif crab_x < pop_crab[0]+100 < crab_x+70 and crab_y < pop_crab[1]+50 < crab_y+100:
                pygame.mixer.Sound.play(pop)
                bullets.remove(pop_crab)
                crab_x = 800-870
                score += 50

        for pop_crab in bombs:
            if crab_x < pop_crab[0]+55 < crab_x+70 and crab_y < pop_crab[1]+70 < crab_y+100:
                pygame.mixer.Sound.play(pop)
                bombs.remove(pop_crab)
                crab_x = 800-870
                score += 50
            elif crab_x < pop_crab[0]+75 < crab_x+70 and crab_y < pop_crab[1]+90 < crab_y+100:
                pygame.mixer.Sound.play(pop)
                bombs.remove(pop_crab)
                crab_x = 800-870
                score += 50

        # spawn karen randomly
        karen_spawn_num = random.randint(0, 100)
        if karen_spawn_num == 50 and not karen_alive and score > 450:
            warning = True

        # show warning before karen spawning
        if warning:
            if warning_once:
                pygame.mixer.Sound.play(alert)
                warning_once = False
            game_display.blit(warning_message, (750, karen_y-15))
            if warning_counter > 45:
                pygame.mixer.Sound.play(whoosh)
                karen_alive = True
                warning_counter = 0
                warning = False
                warning_once = True
            else:
                warning_counter += 1

        # karen movement
        if karen_alive:
            karen_x -= 30
        if karen_x < 0-100:
            karen_hit_player = False
            karen_alive = False
            karen_x = 800
            karen_y = random.randint(0, 400)

        # spawn gringo randomly
        gringo_spawn_num = random.randint(0, 100)
        if not gringo_alive and score > 250 and gringo_spawn_num == 50:
            gringo_alive = True
            gringo.x = 800

        # spawn fatjoe randomly
        fatjoe_spawn_num = random.randint(0, 200)
        if score > 700 and fatjoe_spawn_num == 100 and not fatjoe_alive:
            fatjoe.x = 800
            fatjoe_alive = True

        if fatjoe.x <= -110:
            fatjoe_alive = False

        # gringo-player bullet collision detection
        for hit_gringo in bullets:
            if gringo.x < hit_gringo[0]+90 < gringo.x+00 \
               or gringo.x < hit_gringo[0]+100 < gringo.y+00:
                if gringo.y < hit_gringo[1]+40 < gringo.y+80 \
                   or gringo.y < hit_gringo[1]+50 < gringo.y+80:
                    if not gringo.x > 600:
                        pygame.mixer.Sound.play(explosion2)
                        score += 150
                        bullets.remove(hit_gringo)
                        gringo.x = -100
                        gringo_alive = False

        # karen-player bullet/bomb collision detection
        for hit_karen in bullets:
            if karen_x < hit_karen[0]+90 < karen_x+100 \
               or karen_x < hit_karen[0]+100 < karen_x+100:
                if karen_y < hit_karen[1]+40 < karen_y+80 \
                   or karen_y < hit_karen[1]+50 < karen_y+80:
                    if not karen_x > 700:
                        pygame.mixer.Sound.play(explosion2)
                        bullets.remove(hit_karen)
                        score += 200
                        karen_hit_player = False
                        karen_alive = False
                        karen_x = 800
                        karen_y = random.randint(0, 400)

        for hit_karen in bombs:
            if karen_x < hit_karen[0]+55 < karen_x+100 \
               or karen_x < hit_karen[0]+65 < karen_x+100:
                if karen_y < hit_karen[1]+70 < karen_y+80 \
                   or karen_y < hit_karen[1]+80 < karen_y+80:
                    if not karen_x > 700:
                        pygame.mixer.Sound.play(explosion2)
                        bombs.remove(hit_karen)
                        score += 200
                        karen_hit_player = False
                        karen_alive = False
                        karen_x = 800
                        karen_y = random.randint(0, 400)

        # fatjoe-player bullet/bomb collision detection
        for hit_fatjoe in bullets:
            if fatjoe.x < hit_fatjoe[0]+90 < fatjoe.x+110 or fatjoe.x < hit_karen[0]+100 < fatjoe.x+110:
                if fatjoe.y < hit_fatjoe[1]+40 < fatjoe.y+70 or fatjoe.y < hit_fatjoe[1]+50 < fatjoe.y+70:
                    if not fatjoe.x > 780:
                        pygame.mixer.Sound.play(explosion2)
                        bullets.remove(hit_fatjoe)
                        score += 200
                        fatjoe_alive = False
                        fatjoe.x = -110

        for hit_fatjoe in bombs:
            if fatjoe.x < hit_fatjoe[0]+55 < fatjoe.x+110 or fatjoe.x < hit_karen[0]+75 < fatjoe.x+110:
                if fatjoe.y < hit_fatjoe[1]+70 < fatjoe.y+70 or fatjoe.y < hit_fatjoe[1]+90 < fatjoe.y+70:
                    if not fatjoe.x > 780:
                        pygame.mixer.Sound.play(explosion2)
                        bombs.remove(hit_fatjoe)
                        score += 200
                        fatjoe_alive = False
                        fatjoe.x = -110

        # player-ballon collision detection
        if crab_x < player.x < crab_x+70 or crab_x < player.x+100 < crab_x+70:
            if crab_y < player.y < crab_y+80 or crab_y < player.y+80 < crab_y+80:
                pygame.mixer.Sound.play(explosion)
                player.damaged = True
                player.health -= 1
                crab_x = 800-870

        # player-gringo rocket collision detection
        for hit_player in gringo.bullets:
            if player.x < hit_player[0] < player.x+100 or player.x < hit_player[0]+40 < player.x+100:
                if player.y < hit_player[1]+40 < player.y+80 or player.y < hit_player[1]+50 < player.y+80:
                    pygame.mixer.Sound.play(explosion)
                    player.damaged = True
                    player.health -= 1
                    gringo.bullets.remove(hit_player)

        # player-fatjoe bullet collision detection
        for hit_player in fatjoe.bullets:
            if player.x < hit_player[0] < player.x+100 or player.x < hit_player[0]+20 < player.x+100:
                if player.y < hit_player[1] < player.y+80 or player.y < hit_player[1]+20 < player.y+80:
                    pygame.mixer.Sound.play(explosion)
                    if not fatjoe.fatjoe_hit_player:
                        player.damaged = True
                        player.health -= 1
                        fatjoe.bullets.remove(hit_player)

        # player-fatjoe collision detection
        if fatjoe.x < player.x < fatjoe.x+110 or fatjoe.x < player.x+100 < fatjoe.x+110:
            if fatjoe.y < player.y < fatjoe.y+70 or fatjoe.y < player.y+80 < fatjoe.y+70:
                if not fatjoe.fatjoe_hit_player:
                    pygame.mixer.Sound.play(explosion)
                    player.damaged = True
                    player.health -= 1
                    fatjoe.fatjoe_hit_player = True

        # player-karen collision detection
        if karen_x < player.x < karen_x+100 or karen_x < player.x+100 < karen_x+100:
            if karen_y < player.y < karen_y+88 or karen_y < player.y+80 < karen_y+88:
                if not karen_hit_player:
                    pygame.mixer.Sound.play(explosion)
                    player.damaged = True
                    player.health -= 1
                    karen_hit_player = True

        game_display.blit(sprites.crab, (crab_x,crab_y))
        if crab_x <= 800 - 870:
            crab_x = 800
            crab_y = random.randint(0, 400)
        else:
            if not player.wreck_start:
                crab_x -= 7

        # draw score
        game_display.blit(message_to_screen("SCORE: {0}".format(score), font, 50, black), (10, 10))

        # draw high score
        if score < highscore_int:
            hi_score_message = message_to_screen("HI-SCORE: {0}".format(highscore_int), font, 50, black)
        else:
            highscore_file = open('highscore.dat', "w")
            highscore_file.write(str(score))
            highscore_file.close()
            highscore_file = open('highscore.dat', "r")
            highscore_int = int(highscore_file.read())
            highscore_file.close()
            hi_score_message = message_to_screen("HI-SCORE: {0}".format(highscore_int), font, 50, yellow)

        hi_score_message_rect = hi_score_message.get_rect()

        game_display.blit(hi_score_message, (800-hi_score_message_rect[2]-10, 10))

        # draw health
        if player.health >= 1:
            game_display.blit(sprites.icon, (10, 50))
            if player.health >= 2:
                game_display.blit(sprites.icon, (10+32+10, 50))
                if player.health >= 3:
                    game_display.blit(sprites.icon, (10+32+10+32+10, 50))

        # god-mode (for quicker testing)
        if godmode:
            score = 1000
            player.health = 3

        # drawing ocean
        pygame.draw.rect(game_display, blue, (0, 500, 800, 100))

        pygame.display.update()

        pygame.display.set_caption("COCOLADY running at " + str(int(clock.get_fps())) + " frames per second.")
        clock.tick(FPS)


main_menu()
game_loop()
pygame.quit()
quit()
