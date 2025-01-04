from pygame.surface import Surface
from pygame import draw

from engine import Engine
from settings import CHUNK_WIDTH, CHUNK_HEIGHT, TILE_SIZE, CHUNK_SIZE, COLORS
from settings import SCALE, OCTAVES, PERSISTENCE, LACUNARITY, SEED

from time import time
from random import randint

from noise import pnoise2


class Chunk:
    def __init__(self, pos, engine: Engine):
        self.surface = Surface(CHUNK_SIZE)
        self.pos = pos

        self.engine = engine

        self.get_chunk()

        # self.surface.fill((randint(1, 255), randint(1, 255), randint(1, 255)))

    def get_chunk(self):
        st = time()

        chunk_offset_x = self.pos[0] * CHUNK_WIDTH
        chunk_offset_y = self.pos[1] * CHUNK_HEIGHT

        for y in range(CHUNK_HEIGHT):
            for x in range(CHUNK_WIDTH):
                world_x = chunk_offset_x + x
                world_y = chunk_offset_y + y

                noise_value = pnoise2(
                    (world_x + SEED) / SCALE,
                    (world_y + SEED) / SCALE,
                    octaves=OCTAVES,
                    persistence=PERSISTENCE,
                    lacunarity=LACUNARITY,
                    repeatx=2 ** 24, repeaty=2 ** 24
                ) + 0.5

                noise_value = max(0, min(1, noise_value))

                if noise_value < 0.3:
                    color = (0, 0, int(255 * (noise_value / 0.3)))
                elif noise_value < 0.6:
                    color = (0, int(255 * (noise_value / 0.6)), 0)
                else:
                    color = (
                        int(160 * noise_value), int(160 * noise_value),
                        int(160 * noise_value))

                # random_chance = randint(1, 100)
                # if random_chance <= 5:
                #     tile = 'grass'
                # elif random_chance <= 15:
                #     tile = 'tall_grass'
                # elif random_chance <= 20:
                #     tile = 'tree'
                # elif random_chance <= 25:
                #     tile = 'stone'
                # elif random_chance == 50:
                #     tile = 'flower'

                pos = (x * TILE_SIZE, y * TILE_SIZE)
                # (int(255 * noise_value), int(255 * noise_value), int(255 * noise_value))
                draw.rect(self.surface, color, (*pos, TILE_SIZE, TILE_SIZE))

                # if tile == 'tree':
                #     age = randint(0, 2)
                #     i = self.engine.images[f'tree_{age}']
                #     self.surface.blit(i, pos)
                #
                # elif 'grass' in tile or 'flower' in tile:
                #
                #     i = self.engine.images[tile]
                #     self.surface.blit(i, pos)
                # elif tile == 'stone':
                #
                #     amount = randint(1, 3)
                #     i = self.engine.images[f'stone_{amount}']
                #     self.surface.blit(i, pos)

        et = time()

        print(f'CHUNK LOADED in {et - st}s')

    def draw(self, surface):
        surface.blit(self.surface, self.pos)
