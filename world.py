import pygame.surface
from pygame import Vector2, mouse, Surface, Rect

from load_image import load_image
from settings import screen_width, screen_height, CENTER, TILE_SIZE

from os import listdir


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

        self.wood = 10
        self.stone = 20
        self.food = 100

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
            'food_storage': load_image('food_storage')
        }

        images = [load_image(s.replace('.png', '')) for s in listdir('assets/sprites')]
        keys = [s.replace('.png', '') for s in listdir('assets/sprites')]

        self.images = dict(zip(keys, images))

        self.offset = Vector2(self.rect.topleft) - Vector2(mouse.get_pos())

        self.buildings_g, self.grass_g, self.trees_g, self.stones_g, self.pathways_g, self.farmland_g = groups
        self.groups = groups

        self.houses = 0
        self.mines = 0
        self.windmills = 0

    def update(self, dt):
        if self.check_moving():
            self.move(dt)

        self.screen.blit(self.surface, (0, 0), self.visible_rect)

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

        self.rect.x = max(screen_width - self.rect.width, min(self.rect.x, 0))
        self.rect.y = max(screen_height - self.rect.height,
                          min(self.rect.y, 0))

        self.visible_rect.topleft = -Vector2(self.rect.topleft)

    def get_offset(self):
        self.offset = Vector2(self.rect.topleft) - Vector2(mouse.get_pos())

