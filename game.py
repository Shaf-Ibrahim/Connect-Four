import pygame
from pygame import display, event

import config

# board = Board(3, 5)
# grid = board.grid
pieces = []
player_turn = 1

pygame.init()

display.set_caption('Connect Four')

screen = display.set_mode((config.SCREEN_SIZE, config.SCREEN_SIZE))

def create_pieces():
    pass

def init():
    create_pieces()

init()


running = True

while running:
    events = event.get()

    for e in events:
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False
    pass
