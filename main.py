#!/usr/bin/env python3
import random
from sys import argv
import pygame

pygame.init()

BG = (3, 9, 51)
GREEN = (24, 184, 112)
WHITE = (255, 255, 255)
font = pygame.font.Font(pygame.font.get_default_font(), 36)


width = 900
height = 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

ball = pygame.Rect(int(width / 2 - 15), int(height / 2 - 15), 30, 30)
player = pygame.Rect(int(width - 20), int(height / 2 - 70), 10, 140)
opponent = pygame.Rect(10, int(height / 2 - 70), 10, 140)

player_speed = 0
opponent_speed = 7
ball_moving = False
score_time = True

player_score = 0
opponent_score = 0

multiplayer = False

level = 1

run = True

BALL_SPEED = 7

ball_speed_x = BALL_SPEED * random.choice((1, -1))
ball_speed_y = BALL_SPEED * random.choice((1, -1))


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

    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1


def start():
    global ball_speed_x, ball_speed_y, ball_moving, score_time

    ball.center = (int(width/2), int(height/2))
    current_time = pygame.time.get_ticks()

    if current_time - score_time < 700:
        number_three = font.render("3", False, WHITE)
        screen.blit(number_three, (int(width/2 - 10), int(height/2 + 20)))
    if 700 < current_time - score_time < 1400:
        number_two = font.render("2", False, WHITE)
        screen.blit(number_two, (int(width/2 - 10), int(height/2 + 20)))
    if 1400 < current_time - score_time < 2100:
        number_one = font.render("1", False, WHITE)
        screen.blit(number_one, (int(width/2 - 10), int(height/2 + 20)))

    if multiplayer == False:
        checkScore()

    if current_time - score_time < 2100:
        ball_speed_y, ball_speed_x = 0, 0
    else:
        ball_speed_x = 7 * random.choice((1, -1))
        ball_speed_y = 7 * random.choice((1, -1))
        score_time = None


def player_move():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= height:
        player.bottom = height


def opponent_move():
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


def random_move_difference():
    if score_time:
        return 1
    return random.randrange(7, 13, 1) / 10


def render_score():
    player_text = font.render(f'{player_score}', False, WHITE)
    screen.blit(player_text, (660, 470))

    opponent_text = font.render(f'{opponent_score}', False, WHITE)
    screen.blit(opponent_text, (600, 470))


def render_level():
    level_text = font.render(f'Level {level}', False, WHITE)
    screen.blit(level_text, (50, 50))


def checkScore():
    global level, player_score, opponent_score, ball_speed_x, ball_speed_y, BALL_SPEED
    if player_score >= 9:
        level += 1
        opponent_score = 0
        player_score = 0
        BALL_SPEED = 1.5 * BALL_SPEED
        ball_speed_x = BALL_SPEED * random.choice((1, -1))
        ball_speed_y = BALL_SPEED * random.choice((1, -1))
        pass
    elif opponent_score >= 9:
        opponent_score = 0
        player_score = 0
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

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                player_speed -= 6
            if e.key == pygame.K_DOWN:
                player_speed += 6
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_UP:
                player_speed += 6
            if e.key == pygame.K_DOWN:
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
    screen.fill(BG)

    ball_move()
    player_move()
    opponent_move()
    if score_time:
        start()

    render_score()
    if multiplayer == False:
        render_level()

    pygame.draw.rect(screen, GREEN, player)
    pygame.draw.rect(screen, GREEN, opponent)
    pygame.draw.ellipse(screen, GREEN, ball)
    pygame.draw.aaline(screen, GREEN, (width / 2, 0), (width / 2, height))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
