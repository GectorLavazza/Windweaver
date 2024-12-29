import random
import time

import pygame
import sys

from cursor import Cursor
from map import Map
from settings import *
from world import World


def main():
    pygame.init()
    pygame.mouse.set_visible(False)

    screen = pygame.display.set_mode((screen_width, screen_height),
                                     pygame.DOUBLEBUF | pygame.SRCALPHA)
    world = World(screen, MAP_SIZE, CENTER)

    cursor_g = pygame.sprite.Group()
    tiles_g = pygame.sprite.Group()

    seed = random.randint(0, 100)
    print(f'seed: {seed}')
    map = Map(world, seed, tiles_g)

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

        screen.fill('black')

        tiles_g.draw(screen)
        tiles_g.update(dt)

        world.update(dt)

        # pygame.draw.rect(screen, 'red', world.rect)
        pygame.draw.rect(screen, 'yellow', tiles_g.sprites()[0])
        pygame.draw.rect(screen, 'yellow', tiles_g.sprites()[-1])

        cursor_g.draw(screen)
        cursor.update()

        pygame.display.flip()
        pygame.display.set_caption(str(pygame.mouse.get_pos()))
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
