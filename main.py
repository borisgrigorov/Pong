#!/usr/bin/env python3
from logging import info
import random
import sys
import pygame
import args
import socketio
import time

pygame.init()

BG = (3, 9, 51)
GREEN = (24, 184, 112)
WHITE = (255, 255, 255)
RED = (255, 100, 100)
font = pygame.font.Font(pygame.font.get_default_font(), 36)
debug_font = pygame.font.Font(pygame.font.get_default_font(), 20)

sio = socketio.Client(logger=False)

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

ball = pygame.Rect(int(width / 2 - 15), int(height / 2 - 15), 30, 30)
player = pygame.Rect(int(width - 20), int(height / 2 - 70), 10, 140)
opponent = pygame.Rect(10, int(height / 2 - 70), 10, 140)

debug = args.isDebug()

if args.isDebug():
    print("Launching in debug mode")

if args.isHelpWanted():
    print("How to use:")
    # TODO: PRINT START ARGUMENTS

online = args.isOnline()

onlineData = {
    "waiting": True,
    "host": None,
    "game": None,
    "myName": "",
    "opponentName": "",
    "info": "Connecting to server..."
}


def setServerInfo(info):
    onlineData["info"] = info


def joinGame(game, name):
    sio.emit("join", {
        "gameId": game,
        "name": name
    })
    onlineData["host"] = False
    onlineData["game"] = game
    onlineData["myName"] = name
    setServerInfo("Joining game")


def createGame(name):
    sio.emit("create", {
        "name": name
    })

@sio.event
def connect():
    print("[Server] Connected to server")

def onGameCreated(data):
    print("Created game with ID: " + data["game"])
    onlineData["waiting"] = True
    onlineData["host"] = True
    onlineData["game"] = data["game"]
    setServerInfo("Game created, waiting for opponent to connect")

def onUserJoined(data):
    print("[Server] User " + data["name"] + " joined")
    onlineData["waiting"] = False
    onlineData["game"] = data["game"]
    setServerInfo("Playing with " + data["name"])

def onGameJoined(data):
    print("[Server] You joined game " + data["game"])
    onlineData["waiting"] = False
    onlineData["host"] = False
    onlineData["game"] = data["game"]
    setServerInfo("Playing")

def onGameData(data):
    #print(data)
    if (data["name"] != onlineData["myName"]):
        opponent.y = data["pos"]
    setServerInfo("Playing with " + data["name"])
    if onlineData["host"] == False:
        print(data)
        ball.x = width - int(data["ball_x"])
        ball.y = data["ball_y"]

if online:
    if(args.areParametersValid()):
        params = args.getParams()
        #try:
        sio.connect("http://" + params["server"])
        sio.on("CREATED", onGameCreated)
        sio.on("JOINED", onUserJoined)
        sio.on("JOIN", onGameJoined)
        sio.on("GAMEDATA", onGameData)
        print("[Server] Connecting to server")
        onlineData["myName"] = params["name"]
        if args.isContainingGameId():
            setServerInfo("Joining game " + params["gameId"])
            joinGame(params["gameId"], params["name"])
            onlineData["game"] = params["gameId"]
            onlineData["myName"] = params["name"]
        else:
            setServerInfo("Creating game...")
            createGame(params["name"])
        #except:
        #    print("Error")
        #    sys.exit()

    else:
        sys.exit()

player_score = 0
opponent_score = 0
current_time = 0
tick_time = 60

multiplayer = False

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
    if (online and onlineData["host"] == True) or (online == False):
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
        if online:
            sio.emit("gamedata", {
                "pos": player.y,
                "name": onlineData["myName"],
                "game": onlineData["game"],
                "ball_x": ball.x,
                "ball_y": ball.y,
                "score_time": score_time,
            })
    if ball.colliderect(player):
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10:
            ball_speed_y *= -1

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
    if online:
        current_time = time.time()

    if current_time - score_time < 700:
        number_three = font.render("3", True, WHITE)
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
        can_move = False
        player_speed = 0
        ball_speed_y, ball_speed_x = 0, 0
        player.y = int(height / 2 - 70)
        opponent.y = int(height / 2 - 70)
    else:
        ball_speed_x = BALL_SPEED * random.choice((1, -1))
        ball_speed_y = BALL_SPEED * random.choice((1, -1))
        score_time = None
        can_move = True


def player_move():
    global ball
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= height:
        player.bottom = height

    if online:
        sio.emit("gamedata", {
            "pos": player.y,
            "name": onlineData["myName"],
            "game": onlineData["game"],
            "ball_x": ball.x,
            "ball_y": ball.y,
        });


def opponent_move():
    if multiplayer:
        opponent.y += opponent_speed

        if opponent.top <= 0:
            opponent.top = 0
        if opponent.bottom >= height:
            opponent.bottom = height
    else:
        if abs(opponent.y - ball.y) >= 5:
            if can_move == True:
                if opponent.top < ball.y:
                    opponent.y += opponent_speed * random_move_difference()
                if opponent.bottom > ball.y:
                    opponent.y -= opponent_speed * random_move_difference()

        if opponent.top <= 0:
            opponent.top = 0
        if opponent.bottom >= height:
            opponent.bottom = height * random_move_difference()


def random_move_difference():
    if score_time:
        return 1
    return random.randrange(8, 12, 1) / 10


def render_score():
    player_text = font.render(str(player_score), True, WHITE)
    screen.blit(player_text, (660, 470))

    opponent_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(opponent_text, (600, 470))


def render_level():
    level_text = font.render('Level ' + str(level), True, WHITE)
    if online:
        level_text = font.render(onlineData["opponentName"], True, WHITE)
    screen.blit(level_text, (50, 50))


def debug_stats():
    if debug == True:
        debug_text = debug_font.render('DEBUG', True, RED)
        screen.blit(debug_text, (width - 120, height - 30))

        ball_SPEED_text = debug_font.render(
            'Speed: ' + str(BALL_SPEED), True, WHITE)
        screen.blit(ball_SPEED_text, (50, 90))

        game_time_text = debug_font.render(
            'Ticks: ' + str(pygame.time.get_ticks()), True, WHITE)
        screen.blit(game_time_text, (50, 115))

        b_speed_text = debug_font.render(
            'Ball speed x: ' + str(ball_speed_x) + ' y: ' + str(ball_speed_y), True, WHITE)
        screen.blit(b_speed_text, (50, 140))

        p_speed_text = debug_font.render(
            'Player speed: ' + str(player_speed), True, WHITE)
        screen.blit(p_speed_text, (50, 165))

        o_speed_text = debug_font.render(
            'Opponent speed: ' + str(opponent_speed), True, WHITE)
        screen.blit(o_speed_text, (50, 190))

        can_move_text = debug_font.render(
            'Can move?: ' + str(can_move), True, WHITE)
        screen.blit(can_move_text, (50, 215))

        ball_xy_text = debug_font.render(
            'Ball x: ' + str(ball.x) + '  y: ' + str(ball.y), True, WHITE)
        screen.blit(ball_xy_text, (50, 240))

        player_y_text = debug_font.render(
            'Player y: ' + str(player.y), True, WHITE)
        screen.blit(player_y_text, (50, 265))

        opponent_y_text = debug_font.render(
            'Opponent y: ' + str(opponent.y), True, WHITE)
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
        ball_speed_y = BALL_SPEED * random.choice((1, -1))
        if not multiplayer:
            opponent_speed = (6 + (level * 1.1))
        else:
            opponent_speed = (6 + (level * 1.05))
    elif opponent_score >= 9:
        opponent_score = 0
        player_score = 0
        level = 1
        BALL_SPEED = 7
        ball_speed_x = BALL_SPEED * random.choice((1, -1))
        ball_speed_y = BALL_SPEED * random.choice((1, -1))
        pass


if(args.isMultiplayer()):
    print("Multiplayer active")
    multiplayer = True
    opponent_speed = 0


def renderServerInfo():
    serverinfo_text = debug_font.render(
        onlineData["info"], True, WHITE)
    screen.blit(serverinfo_text, (50, 90))


while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN:
            if can_move == True:
                if e.key == pygame.K_UP:
                    player_speed -= (6 + (level * 1.05))
                if e.key == pygame.K_DOWN:
                    player_speed += (6 + (level * 1.05))
            if debug == True:
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
                player_speed = 0
            if e.key == pygame.K_DOWN:
                player_speed = 0
        if multiplayer:
            if e.type == pygame.KEYDOWN:
                if can_move == True:
                    if e.key == pygame.K_w:
                        opponent_speed -= (6 + (level * 1.05))
                    if e.key == pygame.K_s:
                        opponent_speed += (6 + (level * 1.05))
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_w:
                    opponent_speed = 0
                if e.key == pygame.K_s:
                    opponent_speed = 0
    screen.fill(BG)

    if online:
        if (onlineData["waiting"] == False):
            ball_move()
            player_move()
            if score_time:
                start()
    else:
        ball_move()
        player_move()
        opponent_move()
        if score_time:
            start()

        render_score()
        if multiplayer == False:
            render_level()
    if online:
        renderServerInfo()
    debug_stats()

    pygame.draw.rect(screen, GREEN, player)
    pygame.draw.rect(screen, GREEN, opponent)
    pygame.draw.ellipse(screen, GREEN, ball)
    pygame.draw.aaline(screen, GREEN, (width / 2, 0), (width / 2, height))

    pygame.display.update()
    clock.tick(tick_time)

pygame.quit()
