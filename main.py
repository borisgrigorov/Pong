#!/usr/bin/env python3
import pygame
pygame.init()

BG = (3, 9, 51)

width = 800
height = 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

level = 1

run = True

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
    screen.fill(BG)
    pygame.display.update()
    clock.tick(60)

pygame.quit()