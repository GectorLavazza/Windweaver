import random
import time

import pygame

from cursor import Cursor
from map import Map
from settings import *

# test comment
def main():
    pygame.init()
    pygame.mouse.set_visible(False)

    screen = pygame.display.set_mode((screen_width, screen_height),
                                     pygame.DOUBLEBUF | pygame.SRCALPHA)
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    cursor_g = pygame.sprite.Group()
    tiles_g = pygame.sprite.Group()

    seed = random.randint(0, 100)
    map = Map(surface, seed, CENTER)

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

        map.update(dt)

        screen.blit(pygame.transform.scale_by(surface, SCALE), (0, 0))

        cursor_g.draw(screen)
        cursor.update()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
