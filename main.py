import asyncio
from sys import exit
from time import time

import pygame
from pygame import Vector2

from cursor import Cursor
from map import Map
from settings import *
from sky import Sky
from ui import Text
from world import World

from particles import create_particles

# /// script
# dependencies = [
# "pygame",
# "noise",
# ]
# ///

async def main():
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
    pygame.display.set_caption('Some Game')

    cursor_g = pygame.sprite.Group()
    buildings_g = pygame.sprite.Group()
    grass_g = pygame.sprite.Group()
    trees_g = pygame.sprite.Group()
    stones_g = pygame.sprite.Group()
    pathways_g = pygame.sprite.Group()
    farmland_g = pygame.sprite.Group()
    light_g = pygame.sprite.Group()
    particles_g = pygame.sprite.Group()

    sky = Sky(screen)
    world = World(screen, MAP_SIZE, CENTER, sky, buildings_g, grass_g, trees_g, stones_g, pathways_g, farmland_g,
                  light_g, particles_g)

    pygame.display.set_icon(pygame.transform.scale_by(world.images['house'], 8))

    map = Map(world, grass_g, trees_g, stones_g)

    cursor = Cursor(cursor_g)

    running = 1
    clock = pygame.time.Clock()

    last_time = time()

    label = Text(screen, 5, 'white', (0, 0))
    build = Text(screen, 5, 'white', (0, HEIGHT), bottom_align=True)
    fps = Text(screen, 5, 'white', (screen_width, HEIGHT), right_align=True, bottom_align=True)

    pause = Text(screen, 20, 'white', CENTER, center_align=True, vertical_center_align=True, shade=False)

    et = time()
    playing = 1

    print(f'Startup time: {et - st}')

    zone_surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)
    zone_surface.set_alpha(40)

    show_zone = True

    overlay = pygame.surface.Surface(screen_size, pygame.SRCALPHA)
    overlay.set_alpha(128)
    overlay.fill('black')

    max_mw_tick = 5
    mw_tick = max_mw_tick

    mode = 0

    while running:
        dt = time() - last_time
        dt *= 60
        last_time = time()

        mw_tick -= dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = 0

                if event.key == pygame.K_ESCAPE:
                    playing = False if playing else True

                if event.key == pygame.K_1:
                    mode = 0
                if event.key == pygame.K_2:
                    mode = 1
                if event.key == pygame.K_3:
                    mode = 2
                if event.key == pygame.K_4:
                    mode = 3
                if event.key == pygame.K_5:
                    mode = 4
                if event.key == pygame.K_6:
                    mode = 5

                if event.key == pygame.K_F10:
                    pygame.display.toggle_fullscreen()

                if event.key == pygame.K_F1:
                    world.movement_type = 1 if world.movement_type == 2 else 2
                if event.key == pygame.K_F2:
                    show_zone = False if show_zone else True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 3):
                    cursor.pressed = True

                if event.button == 2:
                    world.get_offset()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button in (1, 3):
                    cursor.pressed = False

            if event.type == pygame.MOUSEWHEEL:
                if mw_tick <= 0:
                    mw_tick = max_mw_tick
                    if event.y == -1:
                        mode = mode + 1 if mode < len(MODES) - 1 else 0
                    elif event.y == 1:
                        mode = mode - 1 if mode > 0 else len(MODES) - 1

        world.current_build = MODES[mode]

        screen.fill('black')

        trees_g.draw(screen)
        stones_g.draw(screen)
        grass_g.draw(screen)
        pathways_g.draw(screen)
        farmland_g.draw(screen)
        buildings_g.draw(screen)
        particles_g.draw(screen)

        if playing:
            world.update(dt)
            trees_g.update(dt)
            stones_g.update(dt)
            grass_g.update(dt)
            pathways_g.update(dt)
            farmland_g.update(dt)
            particles_g.update(dt)

            sky.update(dt)

            if show_zone:
                screen.blit(world.zone_outline_surface, Vector2(world.rect.topleft) - world.zone_offset)

            buildings_g.update(dt)

            # if sky.dark:
            #     light_g.update(screen)

        label.update(f'Wood:{world.wood}/{world.max_wood} Stone:{world.stone}/{world.max_stone} Day:{sky.day} Time: {sky.time}')
        build.update(world.current_build)
        fps.update(f'FPS:{round(clock.get_fps())}')

        if not playing:
            screen.blit(overlay, (0, 0))
            pause.update('Paused')

        cursor_g.draw(screen)
        cursor.update()

        # create_particles(BLACK, pygame.mouse.get_pos(), 10, 120, particles_g)

        pygame.display.update(pygame.Rect(0, 0, WIDTH, HEIGHT))
        clock.tick()

        await asyncio.sleep(0)

    pygame.quit()
    exit()


if __name__ == '__main__':
    asyncio.run(main())
