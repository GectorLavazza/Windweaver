from sys import exit
from time import time

import pygame

from cursor import Cursor
from engine import Engine
from settings import *
from sky import Sky
from ui import Text
from world import World


def main():
    st = time()

    pygame.init()
    pygame.mouse.set_visible(False)
    pygame.event.set_allowed(
        [pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN,
         pygame.MOUSEBUTTONUP])

    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.load('assets/music/windweaver.wav')
    pygame.mixer.music.play(-1)

    flags = pygame.DOUBLEBUF | pygame.SCALED
    screen = pygame.display.set_mode(screen_size, flags, depth=8, vsync=1)

    engine = Engine()

    sky = Sky(screen)
    world = World(screen, CENTER, sky, engine)

    cursor_g = pygame.sprite.Group()

    cursor = Cursor(engine, cursor_g)

    running = 1
    clock = pygame.time.Clock()

    last_time = time()

    resources = Text(screen, 10, 'white', (0, 0))
    fps = Text(screen, 10, 'white', (screen_width, 0),
               right_align=True)

    et = time()

    print(f'Startup time: {et - st}')

    while running:
        dt = time() - last_time
        dt *= 60
        last_time = time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = 0

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

        # tiles_g.draw(screen)
        # tiles_g.update(dt)

        sky.update(dt)

        resources.update(f'{len(world.chunks)} chunks')
        fps.update(f'FPS:{round(clock.get_fps())}')

        cursor_g.draw(screen)
        cursor.update()

        pygame.display.flip()
        pygame.display.set_caption(str(world.camera_pos))
        clock.tick()

    pygame.quit()
    exit()


if __name__ == '__main__':
    main()
