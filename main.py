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
    pygame.display.set_icon(pygame.transform.scale_by(engine.images['house'], 8))

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

    print(f'Startup time: {time() - st}')
    print('[F12] - toggle fullscreen')

    mouse_pos_set = False
    set_to_center = False

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

                if event.key == pygame.K_F12:
                    pygame.display.toggle_fullscreen()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 3):
                    cursor.pressed = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button in (1, 3):
                    cursor.pressed = False

        screen.fill('black')

        if not mouse_pos_set:
            pygame.mouse.set_pos((0, 0))
            mouse_pos_set = True

        world.update(dt)

        if not set_to_center:
            pygame.mouse.set_pos(CENTER)
            set_to_center = True

        sky.update(dt)

        resources.update(f'{len(world.chunks)} chunks')
        fps.update(f'FPS:{round(clock.get_fps())}')

        cursor_g.draw(screen)
        cursor.update()

        pygame.display.flip()
        pygame.display.set_caption('Some Game with Procedural Generation')
        clock.tick()

    pygame.quit()
    exit()


if __name__ == '__main__':
    main()

