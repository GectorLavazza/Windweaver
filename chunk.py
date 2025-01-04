from pygame.surface import Surface
from pygame import draw, Rect, mouse, SRCALPHA
from pygame.sprite import Group, Sprite

from engine import Engine
from settings import CHUNK_WIDTH, CHUNK_HEIGHT, TILE_SIZE, CHUNK_SIZE, COLORS
from settings import SCALE, OCTAVES, PERSISTENCE, LACUNARITY, SEED

from time import time
from random import randint

from noise import pnoise2


class TestTile(Sprite):
    def __init__(self, pos, chunk, color, *group):
        super().__init__(*group)
        self.image = Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.chunk = chunk
        self.rect.topleft = pos
        self.pos = pos

    def update(self, dt):
        self.rect.topleft = (self.pos[0] + self.chunk.rect.x,
                             self.pos[1] + self.chunk.rect.y)
        self.handle_mouse()

    def draw_hover(self):
        self.chunk.world.screen.blit(self.chunk.engine.hover_outline,
                              self.rect.topleft)

    def draw_pressed(self):
        self.chunk.world.screen.blit(self.chunk.engine.pressed_outline,
                                     self.rect.topleft)

    def handle_mouse(self):
        mouse_pos = mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if mouse.get_pressed()[0] or mouse.get_pressed()[2]:
                self.draw_pressed()
            else:
                self.draw_hover()


class Chunk:
    def __init__(self, pos, world, engine: Engine):
        self.surface = Surface(CHUNK_SIZE, SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        self.rect = self.surface.get_rect()
        self.pos = pos
        self.world = world

        self.group = Group()
        self.engine = engine

        self.get_chunk()

        draw.rect(self.surface,
                  (randint(1, 255),
                   randint(1, 255),
                   randint(1, 255)),
                  self.rect, 1)

        # self.surface.fill((randint(1, 255), randint(1, 255), randint(1, 255)))

    def get_chunk(self):
        # st = time()

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

                pos = (x * TILE_SIZE, y * TILE_SIZE)
                TestTile(pos, self, color, self.group)
                # draw.rect(self.surface, color, (*pos, TILE_SIZE, TILE_SIZE))

        # et = time()

        # print(f'CHUNK LOADED in {et - st}s')

    def update(self, dt):
        self.rect.topleft = (
            self.pos[0] * CHUNK_WIDTH * TILE_SIZE - self.world.camera_pos.x,
            self.pos[1] * CHUNK_HEIGHT * TILE_SIZE - self.world.camera_pos.y)

        if self.rect.colliderect(self.world.screen_rect):
            self.group.update(dt)
            self.group.draw(self.world.screen)

            self.world.screen.blit(self.surface, self.rect.topleft)
