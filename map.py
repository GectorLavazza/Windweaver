import noise
import time

from world import World
from settings import *
from tile import Tile

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

                if noise_value < 0.3:
                    tile = 'grass'
                elif noise_value < 0.5:
                    tile = 'tall_grass'
                elif noise_value < 0.7:
                    tile = 'tree'
                else:
                    tile = 'house'

                if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                    pos = (x * TILE_SIZE * SCALE, y * TILE_SIZE * SCALE)
                    sprite = Tile(tile, pos, self.world, self.tiles_g)

                row.append(tile)

            print(f'loading: {round((y + 1) / MAP_HEIGHT * 100, 2)}%')

            tiles.append(row)

        et = time.time()

        print('MAP LOADED')
        print(f'loading time: {et - st}')

        return tiles
