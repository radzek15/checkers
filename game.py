import pygame as pg
from pygame.locals import *
from checkers.GUI import GUI

def game():
    pg.init()

    DISPLAY = pg.display.set_mode((800, 800))
    pg.display.set_caption("checkers")
    clock = pg.time.Clock()

    while True:
        DISPLAY.fill((0, 0, 0))

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()

        pg.display.update()
        clock.tick(60)

game()
