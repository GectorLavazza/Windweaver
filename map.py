import noise
import pygame

from settings import *


class Map:
    def __init__(self, screen: pygame.surface.Surface, seed, camera_pos):
        self.scale = 40.0
        self.octaves = 4
        self.persistence = 0.4
        self.lacunarity = 2.0

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.seed = seed

        self.array = self.get_array()

        self.default_surface = self.get_surface(self.array)
        self.surface = self.get_surface(self.array)

        self.rect = self.surface.get_rect()
        self.rect.center = camera_pos
        self.pos = self.rect.topleft

        self.camera_pos = camera_pos

        self.speed = 1
        self.zoom_speed = 0.01
        self.zoom_factor = 1
        self.dz = 0

        self.dx = 0
        self.dy = 0
        self.velocity = pygame.Vector2(0, 0)

    def update(self, dt):
        self.screen.blit(self.surface, self.pos)
        self.move(dt)

    def move(self, dt):
        input_direction = pygame.Vector2(self.dx, self.dy)

        if input_direction.length() > 0:
            input_direction = input_direction.normalize()

        self.velocity.x = input_direction.x * self.speed * dt
        self.velocity.y = input_direction.y * self.speed * dt

        self.rect.centerx += self.velocity.x * dt
        self.rect.centery += self.velocity.y * dt

        self.camera_pos = self.rect.center
        self.pos = self.rect.topleft

    def zoom(self):
        self.zoom_factor += self.zoom_speed * self.dz
        if self.zoom_factor < MIN_ZOOM:
            self.zoom_factor = MIN_ZOOM
        elif self.zoom_factor > MAX_ZOOM:
            self.zoom_factor = MAX_ZOOM

        zoomed_surface = pygame.transform.smoothscale_by(self.default_surface, self.zoom_factor).convert()
        zoomed_rect = zoomed_surface.get_rect()
        zoomed_rect.center = self.camera_pos
        sides = self.get_sides(zoomed_rect)

        if not any([self.screen_rect.collidepoint(p) for p in sides]):
            self.surface = zoomed_surface

            self.rect = self.surface.get_rect()
            self.rect.center = self.camera_pos
            self.pos = self.rect.topleft

    def get_array(self):
        array = []
        for y in range(MAP_HEIGHT):
            row = []
            for x in range(MAP_WIDTH):

                noise_value = noise.pnoise2(
                    (x + self.seed) / self.scale, (y + self.seed) / self.scale,
                    octaves=self.octaves,
                    persistence=self.persistence,
                    lacunarity=self.lacunarity,
                    repeatx=1024, repeaty=1024
                )

                if noise_value < -0.1:
                    row.append("water")
                elif noise_value < 0.4:
                    row.append("grass")
                else:
                    row.append("mountain")

            array.append(row)

        return array

    def get_surface(self, array):
        w, h = TILE_SIZE * MAP_WIDTH, TILE_SIZE * MAP_HEIGHT
        surface = pygame.surface.Surface((w, h))

        for y in range(h // TILE_SIZE):
            for x in range(w // TILE_SIZE):

                if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                    terrain_type = array[y][x]

                    if terrain_type == "water":
                        color = WATER_COLOR
                    elif terrain_type == "grass":
                        color = GRASS_COLOR
                    else:
                        color = MOUNTAIN_COLOR

                    pygame.draw.rect(surface, color, (
                        x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        return surface

    def get_corners(self, rect: pygame.Rect):
        corners = [rect.topleft, rect.topright,
                   rect.bottomleft, rect.bottomright]

        return corners

    def get_sides(self, rect: pygame.Rect):
        top = [(rect.topleft[0] + i, rect.topleft[1]) for i in range(rect.top // 2 + 1)]
        bottom = [(rect.bottomleft[0] + i, rect.bottomleft[1]) for i in range(rect.top // 2 + 1)]
        right = [(rect.topright[0], rect.topright[1] + i) for i in range(rect.left // 2 + 1)]
        left = [(rect.topleft[0], rect.topleft[1] + i) for i in range(rect.left // 2 + 1)]

        res = top + bottom + right + left

        return res
