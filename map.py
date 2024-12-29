import noise
import time

from utils import get_neighbour_matrix
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

                if noise_value < 0.2:
                    tile = 'fertile_soil2'
                elif noise_value < 0.4:
                    tile = 'fertile_soil'
                elif noise_value < 0.5:
                    tile = 'soil'
                elif noise_value < 0.6:
                    tile = 'soil2'
                elif noise_value < 0.65:
                    tile = 'soil3'
                elif noise_value < 0.8:
                    tile = 'dry_soil'
                elif noise_value < 0.85:
                    tile = 'dry_soil2'
                elif noise_value < 0.9:
                    tile = 'dry_soil3'
                elif noise_value < 0.95:
                    tile = 'bad_soil'
                else:
                    tile = 'bad_soil2'

                row.append(tile)

            # print(f'Iteration 1: {round((y + 1) / MAP_HEIGHT * 100, 2)}%')

            tiles.append(row)

        sprites = []
        for y in range(MAP_HEIGHT):
            row = []

            for x in range(MAP_WIDTH):
                tile = tiles[y][x]

                neighbours = get_neighbour_matrix(tiles, x, y)
                if tile == 'fertile_soil':
                    if neighbours[2][1] == 'soil':
                        tile = 'fertile_soil_bottom'
                        tiles[y][x] = tile
                    elif neighbours[1][2] == 'soil':
                        tile = 'fertile_soil_right'
                        tiles[y][x] = tile
                    elif neighbours[1][0] == 'soil':
                        tile = 'fertile_soil_left'
                        tiles[y][x] = tile

                if tile == 'soil':
                    if 'fertile_soil' in neighbours[2][1]:
                        tile = 'soil_bottom'
                        tiles[y][x] = tile

                if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                    pos = (x * TILE_SIZE * SCALE, y * TILE_SIZE * SCALE)
                    sprite = Tile(tile, pos, self.world, self.tiles_g)

                row.append(sprite)

            # print(f'Iteration 2: {round((y + 1) / MAP_HEIGHT * 100, 2)}%')

            sprites.append(row)

        et = time.time()

        print('MAP LOADED')
        print(f'loading time: {et - st}')

        return tiles
