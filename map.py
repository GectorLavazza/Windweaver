from random import randint

from settings import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE
from tile import Grass, Stone, Tree
from world import World


class Map:
    def __init__(self, world: World, *groups):
        self.scale = 10.0
        self.octaves = 5
        self.persistence = 0.55
        self.lacunarity = 5

        self.world = world
        self.screen_rect = world.rect

        self.seed = randint(0, 100)
        print(f'seed: {self.seed}')

        self.grass_g, self.trees_g, self.stones_g = groups

        self.get_map()

    def get_map(self):
        from random import randint
        import time

        st = time.time()

        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):

                import noise
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

                if randint(1, 5) == 1:
                    tile = 'grass'
                elif randint(1, 10) == 1:
                    tile = 'tall_grass'
                elif randint(1, 50) == 1:
                    tile = 'tree'
                elif randint(1, 100) == 1:
                    tile = 'stone'

                pos = (x * TILE_SIZE, y * TILE_SIZE)

                if tile == 'tree':
                    age = randint(0, 2)
                    Tree(pos, self.world, age, self.trees_g)

                elif 'grass' in tile or 'flower' in tile:
                    Grass(tile, pos, self.world, self.grass_g)

                elif tile == 'stone':
                    amount = randint(1, 3)
                    Stone(pos, self.world, amount, self.stones_g)

            print(f'Loading: {round((y + 1) / MAP_HEIGHT * 100, 2)}%')

        et = time.time()

        print('MAP LOADED')
        print(f'World loading time: {et - st}')
