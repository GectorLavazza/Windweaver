import random
import time

import pygame
import sys

from cursor import Cursor
from map import Map
from settings import *

# test comment
def main():
    pygame.init()
    pygame.mouse.set_visible(False)

    screen = pygame.display.set_mode((screen_width, screen_height),
                                     pygame.DOUBLEBUF | pygame.SRCALPHA)

    cursor_g = pygame.sprite.Group()
    tiles_g = pygame.sprite.Group()

    seed = random.randint(0, 100)
    print(f'seed: {seed}')
    map = Map(screen, seed, CENTER, tiles_g)

    cursor = Cursor(cursor_g)

    running = True
    clock = pygame.time.Clock()

    last_time = time.time()

    while running:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 3):
                    cursor.pressed = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button in (1, 3):
                    cursor.pressed = False

            # if event.type == pygame.MOUSEWHEEL:
            #     map.dz = event.y
            #     map.zoom()

        screen.fill('black')

        map.update(dt)
        # tiles_g.update(screen, dt)

        # tiles_g.draw(screen)

        cursor_g.draw(screen)
        cursor.update()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
