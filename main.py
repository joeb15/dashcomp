import pygame as pg
import sys
from classes import Variables

if not 'jeep_vars' in sys.modules.keys():
    sys.modules['jeep_vars'] = Variables()
variables = sys.modules['jeep_vars']

mousePos = (None, None)
mouseDown = [False]*8

width, height = 800, 480
bg_scale = 1


def setup_display():
    global screen, image
    pg.init()
    pg.mouse.set_visible(False)
    screen = pg.display.set_mode((width, height))
    image = pg.transform.scale(pg.image.load('bg.png'), ((int)(width*bg_scale), (int)(height*bg_scale)))


def loop():
    global mousePos, mouseDown, screen
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEMOTION:
                mousePos = event.pos
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseDown[event.button] = True
            elif event.type == pg.MOUSEBUTTONUP:
                mouseDown[event.button] = False
        screen.blit(image, ((int)(width-width*bg_scale)/2,(int)(height-height*bg_scale)/2))
        pg.display.flip()
        pg.time.wait(100)


if __name__ == "__main__":
    setup_display()
    loop()
