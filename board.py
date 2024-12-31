import random
import time

import pygame
import numpy as np
import sys

from cursor import Cursor
from map import Map
from settings import *
from world import World
from sky import Sky

import noise
from ui import Text


class Board:
    def __init__(self, screen, world, seed):
        self.screen = screen
        self.world = world

        self.scale = 10.0
        self.octaves = 5
        self.persistence = 0.55
        self.lacunarity = 5

        self.seed = seed

        self.map = self.get_map()

    def update(self, dt):
        colors = [pygame.Color('black'), pygame.Color('white')]

        self.map = self.next_population(self.map)

        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                pygame.draw.rect(self.screen, colors[self.map[y][x]], (
                    x * TILE_SIZE * SCALE,
                    y * TILE_SIZE * SCALE,
                    TILE_SIZE * SCALE, TILE_SIZE * SCALE))

    def get_cell(self, mouse_pos):
        cell_x = mouse_pos[0] // TILE_SIZE * SCALE
        cell_y = mouse_pos[1] // TILE_SIZE * SCALE
        if cell_x < 0 or cell_x >= MAP_WIDTH * TILE_SIZE or \
                cell_y < 0 or cell_y >= MAP_HEIGHT * TILE_SIZE:
            return
        return cell_x, cell_y

    def on_click(self, cell):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def next_population(self, population):
        neighbors = sum([
            np.roll(np.roll(population, -1, 1), 1, 0),
            np.roll(np.roll(population, 1, 1), -1, 0),
            np.roll(np.roll(population, 1, 1), 1, 0),
            np.roll(np.roll(population, -1, 1), -1, 0),
            np.roll(population, 1, 1),
            np.roll(population, -1, 1),
            np.roll(population, 1, 0),
            np.roll(population, -1, 0)
        ])
        return (neighbors == 3) | (population & (neighbors == 2))

    def get_map(self):
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

                if noise_value < 0.5:
                    tile = 0
                else:
                    tile = 1

                row.append(tile)

            tiles.append(row)

        return tiles


def main():
    pygame.init()
    pygame.mouse.set_visible(False)

    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.load('assets/music/windweaver.wav')
    pygame.mixer.music.play(-1)

    light_g = pygame.sprite.Group()

    screen = pygame.display.set_mode(screen_size,
                                     pygame.DOUBLEBUF | pygame.SRCALPHA)
    sky = Sky(screen)
    world = World(screen, MAP_SIZE, CENTER, light_g, sky)

    fps = Text(screen, screen_size, 6, 'white', (screen_width, 0),
               right_align=True)

    cursor_g = pygame.sprite.Group()

    seed = random.randint(0, 100)
    print(f'seed: {seed}')
    board = Board(world.surface, world, seed)

    cursor = Cursor(cursor_g)

    running = True
    clock = pygame.time.Clock()

    last_time = time.time()

    while running:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 3):
                    cursor.pressed = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button in (1, 3):
                    cursor.pressed = False

        screen.fill('black')

        world.update(dt)
        board.update(dt)

        fps.update(f'FPS:{round(clock.get_fps())}')

        cursor_g.draw(screen)
        cursor.update()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


main()
