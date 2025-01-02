import random
import time

import pygame
import sys

from cursor import Cursor
from map import Map
from settings import *
from world import World
from sky import Sky

from ui import Text


def main():
    pygame.init()
    pygame.mouse.set_visible(False)

    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.load('assets/music/windweaver.wav')
    pygame.mixer.music.play(-1)

    screen = pygame.display.set_mode(screen_size,
                                     pygame.DOUBLEBUF | pygame.SRCALPHA)
    sky = Sky(screen)
    world = World(screen, MAP_SIZE, CENTER, sky)

    cursor_g = pygame.sprite.Group()
    tiles_g = pygame.sprite.Group()

    seed = random.randint(0, 100000)
    print(f'seed: {seed}')
    map = Map(world, seed, tiles_g)

    cursor = Cursor(cursor_g)

    running = True
    clock = pygame.time.Clock()

    last_time = time.time()

    resources = Text(screen, screen_size, 6, 'white', (0, 0))
    fps = Text(screen, screen_size, 6, 'white', (screen_width, 0),
               right_align=True)

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

                if event.key == pygame.K_1:
                    world.current_build = 'house'
                if event.key == pygame.K_2:
                    world.current_build = 'mine'
                if event.key == pygame.K_3:
                    world.current_build = 'windmill'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 3):
                    cursor.pressed = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button in (1, 3):
                    cursor.pressed = False

        screen.fill('black')

        world.update(dt)

        tiles_g.draw(screen)
        tiles_g.update(dt)

        sky.update(dt)

        resources.update(f'W:{world.wood} S:{world.stone} F:{world.food}')
        fps.update(f'FPS:{round(clock.get_fps())}')

        cursor_g.draw(screen)
        cursor.update()

        pygame.display.flip()
        clock.tick()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
