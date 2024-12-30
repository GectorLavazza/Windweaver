import random

import noise
import time

from utils import get_neighbour_matrix
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
        self.map = self.get_map()

    def get_map(self):
        st = time.time()

        tiles = []

        for y in range(MAP_HEIGHT):
            row = []

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

                if noise_value < 0.4:
                    tile = 'grass'
                elif noise_value < 0.5:
                    tile = 'tall_grass'
                elif noise_value < 0.7:
                    tile = 'tree'
                elif noise_value < 0.75:
                    tile = 'grass'
                elif noise_value < 0.8:
                    tile = 'stones'
                elif noise_value < 0.85:
                    tile = 'tall_grass'
                else:
                    tile = 'grass'

                if random.randint(1, 200) == 1:
                    tile = 'stones'
                elif random.randint(1, 500) == 1:
                    tile = 'flower'

                if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                    pos = (x * TILE_SIZE * SCALE, y * TILE_SIZE * SCALE)

                    if tile == 'tree':
                        if random.randint(1, 5) == 1:
                            tile = 'grass'
                        elif random.randint(1, 100) == 1:
                            tile = 'stones'
                        else:
                            if random.randint(1, 5) == 1:
                                age = 0
                            elif random.randint(1, 5) == 1:
                                age = 2
                            else:
                                age = 1
                            Tree(pos, self.world, age, self.tiles_g)

                    if 'grass' in tile or 'flower' in tile:
                        if tile == 'tall_grass' and random.randint(1, 5) == 1:
                            tile = 'grass'
                        elif tile == 'grass' and random.randint(1, 10) == 1:
                            tile = 'tall_grass'
                        Grass(tile, pos, self.world, self.tiles_g)

                    if tile == 'stones':
                        Stones(pos, self.world, self.tiles_g)

                row.append(tile)

            print(f'Loading: {round((y + 1) / MAP_HEIGHT * 100, 2)}%')

            tiles.append(row)

        et = time.time()

        print('MAP LOADED')
        print(f'Time: {et - st}')

        return tiles
