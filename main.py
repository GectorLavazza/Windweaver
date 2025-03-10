import asyncio
import json
import os.path
from sys import exit
from time import time

import pygame
from pygame import Vector2

from cursor import Cursor
from light import Light
from map import Map
from settings import *
from sky import Sky
from ui import Text, Clock, Resources, Hotbar, Health
from world import World

from tile import *


async def main():
    st = time()

    pygame.init()
    pygame.mouse.set_visible(False)
    pygame.event.set_allowed(
        [pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN,
         pygame.MOUSEBUTTONUP])

    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.load(os.path.join(PATH, 'assets/music/windweaver.wav'))
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

    cursor = Cursor(cursor_g)
    sky_clock = Clock(screen, 20, sky, world)

    top_bg = pygame.Surface((WIDTH, VIGNETTE_WIDTH * SCALE), pygame.SRCALPHA)
    for i in range(top_bg.height, -1, -1):
        pygame.draw.line(top_bg, (0, 0, 0, max(0, min(i * (VIGNETTE_WIDTH * SCALE / (VIGNETTE_WIDTH * 4)) ** -1, 255))),
                         (0, top_bg.height - i), (WIDTH, top_bg.height - i))

    bottom_bg = pygame.Surface((WIDTH, VIGNETTE_WIDTH * SCALE), pygame.SRCALPHA)
    for i in range(bottom_bg.height, -1, -1):
        pygame.draw.line(bottom_bg,
                         (0, 0, 0, max(0, min(i * (VIGNETTE_WIDTH * SCALE / (VIGNETTE_WIDTH * 4)) ** -1, 255))), (0, i),
                         (WIDTH, i))

    right_bg = pygame.Surface((VIGNETTE_WIDTH * SCALE, HEIGHT), pygame.SRCALPHA)
    for i in range(right_bg.width, -1, -1):
        pygame.draw.line(right_bg,
                         (0, 0, 0, max(0, min(i * (VIGNETTE_WIDTH * SCALE / (VIGNETTE_WIDTH * 4)) ** -1, 255))), (i, 0),
                         (i, HEIGHT))

    left_bg = pygame.Surface((VIGNETTE_WIDTH * SCALE, HEIGHT), pygame.SRCALPHA)
    for i in range(left_bg.width, -1, -1):
        pygame.draw.line(left_bg,
                         (0, 0, 0, max(0, min(i * (VIGNETTE_WIDTH * SCALE / (VIGNETTE_WIDTH * 4)) ** -1, 255))),
                         (left_bg.width - i, 0), (left_bg.width - i, HEIGHT))

    running = 1
    clock = pygame.time.Clock()

    last_time = time()

    label = Text(screen, 5, 'white', (0, 150), bottom_align=True, shade=True)
    fps = Text(screen, 5, 'white', (screen_width, HEIGHT), right_align=True, bottom_align=True)

    pause = Text(screen, 20, 'white', CENTER, center_align=True, vertical_center_align=True, shade=False)
    score = Text(screen, 10, 'white', (CENTER[0], 10), center_align=True, shade=False)

    et = time()
    playing = 1

    print(f'Startup time: {round(et - st, 4)}')

    zone_surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)
    zone_surface.set_alpha(40)

    show_zone = True

    overlay = pygame.surface.Surface(screen_size, pygame.SRCALPHA)
    overlay.set_alpha(128)
    overlay.fill('black')

    max_mw_tick = 5
    mw_tick = max_mw_tick

    mode = 0

    resources = Resources(screen, world)
    hotbar = Hotbar(screen, world)

    light = Light(screen, 100, (6, 6, 1), 5)
    light_on = False

    vignette_on = True
    debug_on = False

    health = Health(screen, world)
    # mode = 'start'

    world_name = 'world'
    new_world = 0  # 1 to create new world, 0 to open world

    if new_world:
        Map(world, grass_g, trees_g, stones_g)
    else:
        with open(os.path.join(PATH, f'worlds/{world_name}.json'), mode='r') as f:
            data = json.load(f)
            for s in data['grass_g']:
                pos = s['pos'][0] * TILE_SIZE, s['pos'][1] * TILE_SIZE
                t = Grass(s['name'], pos, world, grass_g)
                t.tick = s['tick']
                t.max_tick = s['max_tick']

            for s in data['trees_g']:
                pos = s['pos'][0] * TILE_SIZE, s['pos'][1] * TILE_SIZE
                t = Tree(pos, world, s['age'], trees_g)
                t.durability = s['durability']
                t.max_durability = s['max_durability']
                t.tick = s['tick']
                t.max_tick = s['max_tick']

            for s in data['stones_g']:
                pos = s['pos'][0] * TILE_SIZE, s['pos'][1] * TILE_SIZE
                t = Stone(pos, world, int(s['name'].split('_')[-1]), stones_g)
                t.amount = s['amount']
                t.durability = s['durability']
                t.max_durability = s['max_durability']

            for s in data['pathways_g']:
                pos = s['pos'][0] * TILE_SIZE, s['pos'][1] * TILE_SIZE
                t = Pathway(pos, world, world.pathways_g)

            for s in data['farmland_g']:
                pos = s['pos'][0] * TILE_SIZE, s['pos'][1] * TILE_SIZE
                t = Farmland(pos, world, world.farmland_g)
                t.name = s['name']
                t.image = world.images[s['name']]
                t.age = s['age']
                t.tick = s['tick']
                t.max_tick = s['max_tick']

            for s in data['buildings_g']:
                pos = s['pos'][0] * TILE_SIZE, s['pos'][1] * TILE_SIZE
                if s['name'] == 'house':
                    t = House(pos, world, buildings_g)
                    t.food = s['food']
                    t.tick = s['tick']
                    t.max_tick = s['max_tick']

                elif s['name'] == 'mine':
                    t = Mine(pos, world, buildings_g)
                    t.start_around = s['start_around']
                    t.collected = s['collected']
                    t.tick = s['tick']
                    t.max_tick = s['max_tick']
                    t.gather_tick = s['gather_tick']
                    t.max_gather_tick = s['max_gather_tick']
                    t.capacity = s['capacity']
                    t.stone = s['stone']

                elif 'windmill' in s['name']:
                    t = Windmill(pos, world, buildings_g)
                    t.name = s['name']
                    t.frame = s['frame']
                    t.collected = s['collected']
                    t.tick = s['tick']
                    t.max_tick = s['max_tick']
                    t.gather_tick = s['gather_tick']
                    t.max_gather_tick = s['max_gather_tick']
                    t.food = s['food']
                    t.animation_tick = s['animation_tick']
                    t.max_animation_tick = s['max_animation_tick']

                elif s['name'] == 'barn':
                    t = Barn(pos, world, buildings_g)
                    t.food = s['food']
                    t.capacity = s['capacity']

                elif s['name'] == 'storage':
                    t = Storage(pos, world, buildings_g)

                elif s['name'] == 'lumberjack':
                    t = Lumberjack(pos, world, buildings_g)
                    t.tick = s['tick']
                    t.max_tick = s['max_tick']
                    t.age_tick = s['age_tick']
                    t.max_age_tick = s['max_age_tick']
                    t.food = s['food']
                    t.grow_tick = s['grow_tick']
                    t.max_grow_tick = s['max_grow_tick']

            world.score = data['world']['score']
            world.wood = data['world']['wood']
            world.max_wood = data['world']['max_wood']
            world.stone = data['world']['stone']
            world.max_stone = data['world']['max_stone']
            world.house_placed = data['world']['house_placed']
            world.current_build = data['world']['current_build']

            sky.tick = data['sky']['tick']
            sky.current_phase = data['sky']['current_phase']
            sky.day = data['sky']['day']

            mode = MODES.index(world.current_build)

    while running:
        dt = time() - last_time
        dt *= 60
        last_time = time()

        mw_tick -= dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and event.key == pygame.KMOD_CTRL:
                    running = 0

                if event.key == pygame.K_ESCAPE:
                    playing = not playing

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
                if event.key == pygame.K_7:
                    mode = 6

                if event.key == pygame.K_e:
                    world.removing = not world.removing

                if event.key == pygame.K_F10:
                    pygame.display.toggle_fullscreen()

                if event.key == pygame.K_F1:
                    world.movement_type = 1 if world.movement_type == 2 else 2
                if event.key == pygame.K_F2:
                    show_zone = not show_zone
                if event.key == pygame.K_F3:
                    light_on = not light_on
                if event.key == pygame.K_F4:
                    vignette_on = not vignette_on
                if event.key == pygame.K_F5:
                    debug_on = not debug_on
                if event.key == pygame.K_F6:
                    world.update_zone()

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
                        world.mouse_d = -1
                        mode = mode + 1 if mode < len(MODES) - 1 else 0
                    elif event.y == 1:
                        world.mouse_d = 1
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

            if light_on:
                light.rect.center = pygame.mouse.get_pos()
                light.update()

        if vignette_on:
            screen.blit(top_bg, (0, 0))
            screen.blit(bottom_bg, (0, HEIGHT - bottom_bg.height))
            screen.blit(right_bg, (WIDTH - right_bg.width, 0))
            screen.blit(left_bg, (0, 0))

        fps.update(f'FPS:{round(clock.get_fps())}')

        if debug_on:
            data = [world.focus.name]
            if 'windmill' in world.focus.name or 'mine' in world.focus.name:
                data.append(f'coll: {world.focus.collected}')
            msg = ' '.join(data)
            label.update(msg)

        resources.update(dt)
        sky_clock.update(dt)
        hotbar.update(dt)
        score.update(world.overall_score)
        # health.update(dt)

        if not playing:
            screen.blit(overlay, (0, 0))
            pause.update('Paused')

        cursor_g.draw(screen)
        cursor.update()

        # create_particles(BLACK, pygame.mouse.get_pos(), 10, 120, particles_g)

        pygame.display.update(pygame.Rect(0, 0, WIDTH, HEIGHT))
        clock.tick()

        await asyncio.sleep(0)

    with open(os.path.join(PATH, f'worlds/{world_name}.json'), mode='w') as f:

        data = {'grass_g': [],
                'trees_g': [],
                'stones_g': [],
                'pathways_g': [],
                'farmland_g': [],
                'buildings_g': []}

        for s in grass_g.sprites():
            data['grass_g'].append(s.save())

        for s in trees_g.sprites():
            data['trees_g'].append(s.save())

        for s in stones_g.sprites():
            data['stones_g'].append(s.save())

        for s in pathways_g.sprites():
            data['pathways_g'].append(s.save())

        for s in farmland_g.sprites():
            data['farmland_g'].append(s.save())

        for s in buildings_g.sprites():
            data['buildings_g'].append(s.save())

        data['world'] = {'wood': world.wood,
                         'max_wood': world.max_wood,
                         'stone': world.stone,
                         'max_stone': world.max_stone,
                         'score': world.score,
                         'current_build': world.current_build,
                         'house_placed': world.house_placed
                         }

        data['sky'] = {'tick': sky.tick,
                       'current_phase': sky.current_phase,
                       'day': sky.day}

        json.dump(data, f)
        print('World successfully saved')

    pygame.quit()
    exit()


if __name__ == '__main__':
    asyncio.run(main())
