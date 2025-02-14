from os import listdir
from random import randint

import pygame.surface
from pygame import Vector2, mouse, Surface, Rect

from load_image import load_image
from settings import screen_width, screen_height, TILE_SIZE, screen_size, SCALE, MAP_WIDTH, MAP_HEIGHT, WHITE


class World:
    def __init__(self, screen: Surface, size, center, sky, *groups):

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.surface = Surface(size)

        self.movement_type = 1

        self.rect = self.surface.get_rect()
        self.rect.center = center

        self.speed = 10
        self.edge_threshold = screen_height // 4

        self.dx = 0
        self.dy = 0
        self.dynamic_speed_x = 0
        self.dynamic_speed_y = 0
        self.velocity = Vector2(0, 0)

        self.wood = 50
        self.stone = 50
        self.max_wood = 50
        self.max_stone = 50
        self.food = 0
        self.max_food = 50

        self.current_build = 'house'

        self.house_placed = False

        self.sky = sky

        self.visible_rect = Rect(0, 0, self.screen.get_width(),
                                 self.screen.get_height())
        self.visible_rect = self.visible_rect.clip(self.surface.get_rect())

        self.hover_outline = Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.hover_outline.fill('white')
        self.hover_outline.set_alpha(60)
        self.pressed_outline = Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.pressed_outline.fill('white')
        self.pressed_outline.set_alpha(100)

        self.build_images = {
            'house': load_image('house'),
            'mine': load_image('mine'),
            'windmill': load_image('windmill_1'),
            'pathway': load_image('pathway'),
            'barn': load_image('barn'),
            'storage': load_image('storage'),
            'lumberjack': load_image('lumberjack')
        }

        images = [load_image(s.replace('.png', '')) for s in listdir('assets/sprites')]
        keys = [s.replace('.png', '') for s in listdir('assets/sprites')]

        self.images = dict(zip(keys, images))

        self.offset = Vector2(self.rect.topleft) - Vector2(mouse.get_pos())

        (self.buildings_g, self.grass_g,
         self.trees_g, self.stones_g,
         self.pathways_g, self.farmland_g,
         self.light_g, self.particles_g) = groups
        self.groups = groups

        self.houses = 0
        self.mines = 0
        self.windmills = 0
        self.barns = 0
        self.pathways = 0
        self.storages = 0
        self.lumberjacks = 0

        self.zone_surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)
        self.zone_pos = Vector2(0, 0)
        self.zone_offset = Vector2(0, 0)

        self.zone_outline_surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)
        self.zone_alpha = 128

        self.removing = False
        self.mouse_d = -1

        self.update_zone()

        self.houses_left = 'inf'
        self.pathways_left = max(0, self.houses * 5 - self.pathways)
        self.mines_left = max(0, self.houses // 4 - self.mines)
        self.windmills_left = max(0, self.houses // 2 - self.windmills)
        self.barns_left = 'inf'
        self.storages_left = 'inf'
        self.lumberjacks_left = max(0, self.houses // 1 - self.lumberjacks)
        self.left = [self.houses_left, self.pathways_left,
                     self.windmills_left, self.barns_left,
                     self.mines_left, self.storages_left, self.lumberjacks_left]

        self.score = 0
        self.buildings_score = 0
        self.overall_score = self.score + self.buildings_score

        self.max_health = 3
        self.health = self.max_health

        self.focus = None

    def update(self, dt):
        self.health = max(0, self.health)

        if self.check_moving():
            self.move(dt)

        # self.screen.blit(self.surface, (0, 0), self.visible_rect)
        self.count_objects()
        self.zone_alpha = max(128, min(int(self.zone_alpha - dt), 255))
        self.zone_outline_surface.set_alpha(self.zone_alpha)

        self.hover_outline.fill('white' if not self.removing else 'red')
        self.pressed_outline.fill('white' if not self.removing else 'red')

        self.houses_left = 'inf'
        self.pathways_left = max(0, self.houses * 5 - self.pathways)
        self.mines_left = max(0, self.houses // 4 - self.mines) + (1 if self.houses // 2 > 0 and self.mines == 0 else 0)
        self.windmills_left = max(0, self.houses // 2 - self.windmills)
        self.barns_left = max(0, self.houses // 3 - self.barns) + (1 if self.barns == 0 else 0)
        self.storages_left = max(0, self.houses // 5 - self.storages) + (1 if self.houses // 2 > 0 and self.storages == 0 else 0)
        self.lumberjacks_left = max(0, self.houses // 1 - self.lumberjacks)
        self.left = [self.houses_left, self.pathways_left, self.windmills_left, self.barns_left,
                     self.mines_left, self.storages_left, self.lumberjacks_left]

        self.buildings_score = self.houses * 5 + self.windmills * 10 + self.mines * 10 + self.barns * 15 + self.storages * 20
        self.overall_score = self.score + self.buildings_score

    def update_zone(self):
        self.zone = [s.zone for s in self.pathways_g.sprites() + self.buildings_g.sprites()]

        self.zone_surface.fill((0, 0, 0, 0))

        for z in self.zone:
            pygame.draw.rect(self.zone_surface, 'green', z)

        mask = pygame.mask.from_surface(self.zone_surface)
        outline = mask.outline()
        self.zone_outline_surface = mask.to_surface()
        self.zone_alpha = 255
        self.zone_outline_surface.set_alpha(self.zone_alpha)
        self.zone_outline_surface.fill((0, 0, 0, 0))
        for p in outline:
            pos = p[0] - 1 * SCALE / 2, p[1] - 1 * SCALE / 2
            pygame.draw.rect(self.zone_outline_surface, WHITE, pygame.Rect(*pos, SCALE, SCALE))
        self.zone_outline_surface.set_colorkey((0, 0, 0, 0))
        self.zone_pos = self.zone_outline_surface.get_rect().topleft
        self.zone_offset = Vector2(self.rect.topleft)

    def check_moving(self):
        mouse_x, mouse_y = mouse.get_pos()

        self.dx = 0
        self.dy = 0

        if mouse_x < self.edge_threshold:
            self.dx = 1

            distance_to_edge = self.edge_threshold - mouse_x
            self.dynamic_speed_x = distance_to_edge / self.edge_threshold

        elif mouse_x > screen_width - self.edge_threshold:
            self.dx = -1

            distance_to_edge = mouse_x - (
                    screen_width - self.edge_threshold)
            self.dynamic_speed_x = distance_to_edge / self.edge_threshold

        if mouse_y < self.edge_threshold:
            self.dy = 1

            distance_to_edge = self.edge_threshold - mouse_y
            self.dynamic_speed_y = distance_to_edge / self.edge_threshold

        elif mouse_y > screen_height - self.edge_threshold:
            self.dy = -1

            distance_to_edge = mouse_y - (
                    screen_height - self.edge_threshold)

            self.dynamic_speed_y = distance_to_edge / self.edge_threshold

        if self.movement_type == 1:
            if mouse.get_pressed()[1]:
                return True
        else:
            if self.dx or self.dy:
                return True

    def count_objects(self):
        self.houses = len(list(filter(lambda b: 'house' in b.name, self.buildings_g.sprites())))
        self.mines = len(list(filter(lambda b: 'mine' in b.name, self.buildings_g.sprites())))
        self.windmills = len(list(filter(lambda b: 'windmill' in b.name, self.buildings_g.sprites())))
        self.barns = len(list(filter(lambda b: 'barn' in b.name, self.buildings_g.sprites())))
        self.storages = len(list(filter(lambda b: 'storage' in b.name, self.buildings_g.sprites())))
        self.pathways = len(self.pathways_g.sprites())
        self.lumberjacks = len(list(filter(lambda b: 'lumberjack' in b.name, self.buildings_g.sprites())))

        self.food = sum([p.food for p in self.buildings_g.sprites() if p.name == 'barn' and p.food > 0])
        self.max_food = 50 + sum([p.capacity for p in self.buildings_g.sprites() if p.name == 'barn'])

        self.max_wood = 50 + sum([p.wood_capacity for p in self.buildings_g.sprites() if p.name == 'storage'])

        self.max_stone = 50 + sum([p.stone_capacity for p in self.buildings_g.sprites() if p.name == 'storage'])

    def move(self, dt):
        mp = mouse.get_pos()

        if self.movement_type == 1:
            self.rect.topleft = self.offset + Vector2(mp)
        else:
            input_direction = Vector2(self.dx, self.dy)
            if input_direction.length() > 0:
                input_direction = input_direction.normalize()

            speed_multiplier_x = max(0, min(1, self.dynamic_speed_x))
            speed_multiplier_y = max(0, min(1, self.dynamic_speed_y))

            self.velocity.x = input_direction.x * self.speed * speed_multiplier_x * dt
            self.velocity.y = input_direction.y * self.speed * speed_multiplier_y * dt

            if self.velocity.length() > self.speed:
                self.velocity = self.velocity.normalize() * self.speed

            self.rect.x += self.velocity.x
            self.rect.y += self.velocity.y

        if MAP_WIDTH > 40 and MAP_HEIGHT > 23:
            self.rect.x = max(screen_width - self.rect.width, min(self.rect.x, 0))
            self.rect.y = max(screen_height - self.rect.height,
                              min(self.rect.y, 0))
        else:
            self.rect.centerx = min(screen_width, max(self.rect.centerx, 0))
            self.rect.centery = min(screen_height, max(self.rect.centery, 0))

        self.visible_rect.topleft = -Vector2(self.rect.topleft)

    def get_offset(self):
        self.offset = Vector2(self.rect.topleft) - Vector2(mouse.get_pos())

    def play_sound(self, filename, volume=0.5):
        sfx = pygame.mixer.Sound(f'assets/sfx/{filename}.wav')
        sfx.set_volume(randint(int(volume * 100 - 5), int(volume * 100 + 5)) / 100)
        sfx.play()
