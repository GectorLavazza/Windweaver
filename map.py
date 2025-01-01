import random

import noise
import time

from world import World
from settings import *
from tile import *


class Map:
    def __init__(self, world: World, seed, tiles_g):
        self.scale = 10.0
        self.octaves = 5
        self.persistence = 0.55
        self.lacunarity = 5

        self.world = world
        self.screen_rect = world.rect

        self.seed = seed

        self.tiles_g = tiles_g

        w, h = TILE_SIZE * MAP_WIDTH * SCALE, TILE_SIZE * MAP_HEIGHT * SCALE
        self.surface = pygame.surface.Surface((w, h)).convert_alpha()

        self.get_map()

    def get_map(self):
        st = time.time()

        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                noise_value = noise.pnoise2(
                    (x + self.seed) / self.scale, (y + self.seed) / self.scale,
                    octaves=self.octaves,
                    persistence=self.persistence,
                    lacunarity=self.lacunarity,
                    repeatx=1024, repeaty=1024
                ) + 0.5

                if noise_value < 0:
                    noise_value = 0
                elif noise_value > 1:
                    noise_value = 1

                if noise_value < 0.42:
                    tile = 'grass'
                elif noise_value < 0.52:
                    tile = 'tall_grass'
                elif noise_value < 0.7:
                    tile = 'tree'
                else:
                    tile = 'stone'

                if random.randint(1, 5) == 1:
                    tile = 'grass'
                elif random.randint(1, 10) == 1:
                    tile = 'tall_grass'
                elif random.randint(1, 50) == 1:
                    tile = 'tree'
                elif random.randint(1, 100) == 1:
                    tile = 'stone'
                elif random.randint(1, 500) == 1:
                    tile = 'flower'

                pos = (x * TILE_SIZE * SCALE, y * TILE_SIZE * SCALE)

                if tile == 'tree':
                    age = random.randint(0, 2)
                    Tree(pos, self.world, age, self.tiles_g)

                elif 'grass' in tile or 'flower' in tile:
                    Grass(tile, pos, self.world, self.tiles_g)

                elif tile == 'stone':
                    amount = random.randint(1, 3)
                    Stone(pos, self.world, amount, self.tiles_g)

            print(f'Loading: {round((y + 1) / MAP_HEIGHT * 100, 2)}%')

        et = time.time()

        print('MAP LOADED')
        print(f'Time: {et - st}')
