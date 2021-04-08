#!/usr/bin/env python3
import random
from sys import argv
import pygame


pygame.init()

BG = (3, 9, 51)
GREEN = (24, 184, 112)
WHITE = (255, 255, 255)
RED = (255, 100, 100)
font = pygame.font.Font(pygame.font.get_default_font(), 36)
debug_font = pygame.font.Font(pygame.font.get_default_font(), 20)


width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

ball = pygame.Rect(int(width / 2 - 15), int(height / 2 - 15), 30, 30)
player = pygame.Rect(int(width - 20), int(height / 2 - 70), 10, 140)
opponent = pygame.Rect(10, int(height / 2 - 70), 10, 140)

debug = False

player_score = 0
opponent_score = 0
current_time = 0
tick_time = 60

level = 1

BALL_SPEED = 7

ball_speed_x = BALL_SPEED * random.choice((1, -1))
ball_speed_y = BALL_SPEED * random.choice((1, -1))

player_speed = 0
opponent_speed = 7.1    
ball_moving = False
score_time = True
can_move = True

run = True

def ball_move():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= height:
        ball_speed_y *= -1

    if ball.left <= 0:
        score_time = pygame.time.get_ticks()
        player_score += 1

    if ball.right >= width:
        score_time = pygame.time.get_ticks()
        opponent_score += 1

    if ball.colliderect(player):
        if abs(ball.right - player.left) < 10:        # Masivní problém šéfe. Ehm. Když je rychlost míč vyšší než 10, míč doslova proletí hráčem či opponentem.
            ball_speed_x *= -1                          # Dočasné řešení je buď místo 10 ho odrazit na BALL_SPEED + 1 nebo změnit bod kde to připočítá bod u řádku 56 až 62
        elif abs(ball.bottom - player.top) < 10:        # Tak či tak nemám perfektní řešení a netuším jak tento problém vyřešit.
            ball_speed_y *= -1                          # Nejlepší řešení by možná bylo, kdyby ta páčka měla hitbox i za hranicí okna a i kdyby byl gól, tak to zkontroluje jestli je to u hitboxu toho hráče/opponenta
        elif abs(ball.top - player.bottom) < 10:        # Pokud by to bylo v hitboxu toho hráče, tak by to ignorovalo tu kondici kde to přičítá bod a prostě by se to odpálilo.
            ball_speed_y *= -1                          # A nebo je možné tam dát limit........

    if ball.colliderect(opponent):
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10:
            ball_speed_y *= -1


def start():
    global ball_speed_x, ball_speed_y, ball_moving, score_time, current_time, can_move, player_speed

    ball.center = (int(width/2), int(height/2))
    current_time = pygame.time.get_ticks()

    if current_time - score_time < 700:
        number_three = font.render("3", True, WHITE)                 # Většina změn u textu je povolený antialiasing
        screen.blit(number_three, (int(width/2 - 10), int(height/2 + 20)))
    if 700 < current_time - score_time < 1400:
        number_two = font.render("2", True, WHITE)
        screen.blit(number_two, (int(width/2 - 10), int(height/2 + 20)))
    if 1400 < current_time - score_time < 2100:
        number_one = font.render("1", True, WHITE)
        screen.blit(number_one, (int(width/2 - 10), int(height/2 + 20)))

    if multiplayer == False:
        checkScore()

    if current_time - score_time < 2100:
        can_move = False                 # can_move je nová proměnná. Dokáže zastavit hráče. Tady konkrétně ho blokuje před začátkem hry
        player_speed = 0
        ball_speed_y, ball_speed_x = 0, 0
        player.y = int(height / 2 - 70)         # Hráče to posadí doprostřed
        opponent.y = int(height / 2 - 70)
    else:
        ball_speed_x = BALL_SPEED * random.choice((1, -1))      # Opraven bug kdy se míč nezrychloval
        ball_speed_y = BALL_SPEED * random.choice((1, -1))
        score_time = None
        can_move = True


def player_move():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= height:
        player.bottom = height


def opponent_move():
<<<<<<< HEAD
    if multiplayer:
        opponent.y += opponent_speed

        if opponent.top <= 0:
            opponent.top = 0
        if opponent.bottom >= height:
            opponent.bottom = height
    else:
        if opponent.top < ball.y:
            opponent.y += opponent_speed * random_move_difference()
        if opponent.bottom > ball.y:
            opponent.y -= opponent_speed * random_move_difference()

        if opponent.top <= 0:
            opponent.top = 0 * 0.8
        if opponent.bottom >= height:
            opponent.bottom = height * random_move_difference()
=======
    global opponent_speed
    if abs(opponent.y - ball.y) >= 15:             # Pokud není rozdíl vzdálenosti na ose y vyšší než 15, destička se vůbec hýbat nebude. Navíc to přidává umělou odezvu co by měl člověk.
        if can_move == True:
            if opponent.top < ball.y:
                opponent.y += opponent_speed * random_move_difference()
            if opponent.bottom > ball.y:
                opponent.y -= opponent_speed * random_move_difference()

    if opponent.top <= 0:
        opponent.top = 0 * 0.8           # Lol na co je toto? Když to oddělám funguje to per
    if opponent.bottom >= height:
        opponent.bottom = height * random_move_difference()
>>>>>>> 5444078 (Debug mode, bug fixy, před začátkem se nemůžeš hýbat)


def random_move_difference():
    if score_time:
        return 1
    return random.randrange(7, 13, 1) / 10


def render_score():
    player_text = font.render(str(player_score), True, WHITE)
    screen.blit(player_text, (660, 470))

    opponent_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(opponent_text, (600, 470))


def render_level():
    level_text = font.render('Level ' + str(level), True, WHITE)
    screen.blit(level_text, (50, 50))
    

def debug_stats():         # Nový debug režim. Ukazuje důležité info a umožňuje cheatování pomocí j, n, k, l
    if debug == True:
        debug_text = debug_font.render('DEBUG', True, RED)
        screen.blit(debug_text, (width - 120, height - 30))

        ball_SPEED_text = debug_font.render('Speed: ' + str(BALL_SPEED), True, WHITE)
        screen.blit(ball_SPEED_text, (50, 90))

        game_time_text = debug_font.render('Ticks: ' + str(pygame.time.get_ticks()), True, WHITE)
        screen.blit(game_time_text, (50, 115))

        b_speed_text = debug_font.render('Ball speed x: ' + str(ball_speed_x) + ' y: ' + str(ball_speed_y), True, WHITE)
        screen.blit(b_speed_text, (50, 140))

        p_speed_text = debug_font.render('Player speed: ' + str(player_speed), True, WHITE)
        screen.blit(p_speed_text, (50, 165))

        o_speed_text = debug_font.render('Opponent speed: ' + str(opponent_speed), True, WHITE)
        screen.blit(o_speed_text, (50, 190))

        can_move_text = debug_font.render('Can move?: ' + str(can_move), True, WHITE)
        screen.blit(can_move_text, (50, 215))

        ball_xy_text = debug_font.render('Ball x: ' + str(ball.x) + '  y: ' + str(ball.y), True, WHITE)
        screen.blit(ball_xy_text, (50, 240))

        player_y_text = debug_font.render('Player y: ' + str(player.y), True, WHITE)
        screen.blit(player_y_text, (50, 265))
        
        opponent_y_text = debug_font.render('Opponent y: ' + str(opponent.y), True, WHITE)
        screen.blit(opponent_y_text, (50, 290))

        tick_text = debug_font.render('Tps: ' + str(tick_time), True, WHITE)
        screen.blit(tick_text, (50, 315))


def checkScore():
    global level, player_score, opponent_score, ball_speed_x, ball_speed_y, BALL_SPEED, opponent_speed
    if player_score >= 9:
        level += 1
        opponent_score = 0
        player_score = 0
        BALL_SPEED = 7 + (1.2 * level)         
        ball_speed_x = BALL_SPEED * random.choice((1, -1))
        ball_speed_y = BALL_SPEED * random.choice((1, -1))    # Další opravení toho bugu kde se míč nezrychloval
        opponent_speed = (6 + (level * 1.05))
    elif opponent_score >= 9:
        opponent_score = 0
        player_score = 0
<<<<<<< HEAD
        level = 1
        BALL_SPEED = 7 * BALL_SPEED
        ball_speed_x = BALL_SPEED * random.choice((1, -1))
        ball_speed_y = BALL_SPEED * random.choice((1, -1))
        pass

print(argv)
if(len(argv) == 2 and argv[1] == "multiplayer"):
    print("Multiplayer active")
    multiplayer = True
    opponent_speed = 0
    pass
=======
        level = 0


>>>>>>> 5444078 (Debug mode, bug fixy, před začátkem se nemůžeš hýbat)

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN:
            if can_move == True:            # Implementace can_move. Před začátkem hry by němelo být možné se hýbat
                if e.key == pygame.K_UP:
                    player_speed -= (6 + (level * 1.05))
                if e.key == pygame.K_DOWN:
                    player_speed += (6 + (level * 1.05))
            if debug == True:               # Event pro debug/cheat režim.
                if e.key == pygame.K_j:
                    opponent_score += 1
                if e.key == pygame.K_n:
                    opponent_score -= 1
                if e.key == pygame.K_k:
                    player_score += 1
                if e.key == pygame.K_m:
                    player_score -= 1
                if e.key == pygame.K_KP_PLUS:
                    tick_time += 5
                if e.key == pygame.K_KP_MINUS:
                    tick_time -= 5
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_UP:
                player_speed = 0            # Kdyby tady bylo -= tak by při změně rychlosti na vyšší mohlo dojít ke zbytku (efekt padajícího odpalovátka); 0 je nejbezpečnější
            if e.key == pygame.K_DOWN:
<<<<<<< HEAD
                player_speed -= 6
        if multiplayer:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_w:
                    opponent_speed -= 6
                if e.key == pygame.K_s:
                    opponent_speed += 6
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_w:
                    opponent_speed += 6
                if e.key == pygame.K_s:
                    opponent_speed -= 6
=======
                player_speed = 0
>>>>>>> 5444078 (Debug mode, bug fixy, před začátkem se nemůžeš hýbat)
    screen.fill(BG)

    ball_move()
    player_move()
    opponent_move()
    if score_time:
        start()

    render_score()
<<<<<<< HEAD
    if multiplayer == False:
        render_level()
=======
    render_level()
    debug_stats()
>>>>>>> 5444078 (Debug mode, bug fixy, před začátkem se nemůžeš hýbat)

    pygame.draw.rect(screen, GREEN, player)
    pygame.draw.rect(screen, GREEN, opponent)
    pygame.draw.ellipse(screen, GREEN, ball)
    pygame.draw.aaline(screen, GREEN, (width / 2, 0), (width / 2, height))

    pygame.display.update()
    clock.tick(tick_time)

pygame.quit()
