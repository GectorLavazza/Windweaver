from sys import exit
from time import time

import pygame

from cursor import Cursor
from map import Map
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
    pygame.display.set_caption('Some Game')

    cursor_g = pygame.sprite.Group()
    buildings_g = pygame.sprite.Group()
    grass_g = pygame.sprite.Group()
    trees_g = pygame.sprite.Group()
    stones_g = pygame.sprite.Group()
    pathways_g = pygame.sprite.Group()
    farmland_g = pygame.sprite.Group()

    sky = Sky(screen)
    world = World(screen, MAP_SIZE, CENTER, sky, buildings_g, grass_g, trees_g, stones_g, pathways_g, farmland_g)

    pygame.display.set_icon(pygame.transform.scale_by(world.images['house'], 8))

    map = Map(world, grass_g, trees_g, stones_g)

    cursor = Cursor(cursor_g)

    running = 1
    clock = pygame.time.Clock()

    last_time = time()

    resources = Text(screen, 5, 'white', (0, 0))
    objects = Text(screen, 5, 'white', (WIDTH, 0), right_align=True)
    build = Text(screen, 5, 'white', (0, HEIGHT), bottom_align=True)
    fps = Text(screen, 5, 'white', (screen_width, HEIGHT), right_align=True, bottom_align=True)

    et = time()

    print(f'Startup time: {et - st}')

    zone_surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)
    zone_surface.set_alpha(40)

    show_zone = False

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
                if event.key == pygame.K_4:
                    world.current_build = 'pathway'
                if event.key == pygame.K_5:
                    world.current_build = 'barn'
                if event.key == pygame.K_6:
                    world.current_build = 'storage'

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

        screen.fill('black')

        world.update(dt)

        trees_g.draw(screen)
        trees_g.update(dt)

        stones_g.draw(screen)
        stones_g.update(dt)

        grass_g.draw(screen)
        grass_g.update(dt)

        pathways_g.draw(screen)
        pathways_g.update(dt)

        farmland_g.draw(screen)
        farmland_g.update(dt)

        buildings_g.draw(screen)
        buildings_g.update(dt)

        zone_surface.fill((0, 0, 0, 0))

        for z in world.zone:
            pygame.draw.rect(zone_surface, 'green', z)

        if show_zone:
            screen.blit(zone_surface, (0, 0))
            a = 255
        else:
            a = 128
        mask = pygame.mask.from_surface(zone_surface)
        outline = mask.outline()
        surface = mask.to_surface()
        surface.fill((0, 0, 0, 0))
        for p in outline:
            pos = p[0] - 1 * SCALE / 2, p[1] - 1 * SCALE / 2
            pygame.draw.rect(surface, (0, 255, 0, a), pygame.Rect(*pos, SCALE, SCALE))
        surface.set_colorkey((0, 0, 0, 0))
        screen.blit(surface, (0, 0))

        sky.update(dt)

        resources.update(f'W:{world.wood}/{world.max_wood} S:{world.stone}/{world.max_stone}')
        objects.update(f'H:{world.houses} M:{world.mines} W:{world.windmills} B:{world.barns}')
        build.update(world.current_build)
        fps.update(f'FPS:{round(clock.get_fps())}')

        cursor_g.draw(screen)
        cursor.update()

        pygame.display.flip()
        clock.tick()

    pygame.quit()
    exit()


if __name__ == '__main__':
    main()
