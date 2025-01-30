import pygame
from pygame import Vector2, mouse, Surface, Rect

from load_image import load_image
from settings import screen_width, screen_height, CENTER, SCALE


class World:
    def __init__(self, screen: Surface, size, sky):

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.surface = Surface(size, pygame.SRCALPHA)
        self.orig_surface = Surface(size, pygame.SRCALPHA)

        self.movement_type = 1

        self.rect = self.surface.get_rect()
        self.rect.center = CENTER

        self.speed = 10 * SCALE
        self.edge_threshold = screen_height // 4

        self.dx = 0
        self.dy = 0
        self.dynamic_speed_x = 0
        self.dynamic_speed_y = 0
        self.velocity = Vector2(0, 0)

        self.wood = 0
        self.stone = 0
        self.food = 100

        self.current_build = 'house'

        self.house_placed = False

        self.houses = 0
        self.mines = 0
        self.windmills = 0

        self.sky = sky

        self.visible_rect = Rect(0, 0, self.screen.get_width(),
                                 self.screen.get_height())
        self.visible_rect = self.visible_rect.clip(self.surface.get_rect())

        self.hover_outline = load_image('hover')
        self.pressed_outline = load_image('pressed')

        self.build_images = {
            'house': load_image('build_house'),
            'mine': load_image('build_mine'),
            'windmill': load_image('windmill_build')
        }

        self.images = {
            'grass': load_image('grass'),
            'tall_grass': load_image('tall_grass'),
            'farmland_0': load_image('farmland_0'),
            'farmland_1': load_image('farmland_1'),
            'farmland_2': load_image('farmland_2'),
            'flower': load_image('flower'),
            'house': load_image('house'),
            'house_light': load_image('house_light'),
            'mine': load_image('mine'),
            'pathway': load_image('pathway'),
            'stone_1': load_image('stone_1'),
            'stone_2': load_image('stone_2'),
            'stone_3': load_image('stone_3'),
            'tree_0': load_image('tree_0'),
            'tree_1': load_image('tree_1'),
            'tree_2': load_image('tree_2'),
            'windmill_1': load_image('windmill_1'),
            'windmill_2': load_image('windmill_2'),
        }

        self.offset = Vector2(self.rect.topleft) - Vector2(mouse.get_pos())
        self.zoom_factor = 1

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

            self.velocity.x = input_direction.x * self.speed * speed_multiplier_x * dt * self.zoom_factor ** -1
            self.velocity.y = input_direction.y * self.speed * speed_multiplier_y * dt * self.zoom_factor ** -1

            if self.velocity.length() > self.speed:
                self.velocity = self.velocity.normalize() * self.speed

            self.rect.x += self.velocity.x
            self.rect.y += self.velocity.y

        # self.rect.x = max(screen_width - self.rect.width, min(self.rect.x, 0))
        # self.rect.y = max(screen_height - self.rect.height,
        #                   min(self.rect.y, 0))

        self.visible_rect.topleft = -Vector2(self.rect.topleft)

    def get_offset(self):
        self.offset = Vector2(self.rect.topleft) - Vector2(mouse.get_pos())

    def zoom(self, d):
            if d == -1 and self.zoom_factor <= 2:
                self.zoom_factor += 0.05
                w = int(self.screen_rect.w * self.zoom_factor)
                h = int(self.screen_rect.h * self.zoom_factor)
                scaled_size = w - w % 2, h - h % 2
                self.surface = pygame.transform.scale(self.orig_surface, scaled_size)
                pos = self.rect.topleft
                self.rect = self.surface.get_rect()
                self.rect.topleft = pos
            elif d == 1 and self.zoom_factor >= 0.5:
                self.zoom_factor -= 0.05

                w = int(self.screen_rect.w * self.zoom_factor)
                h = int(self.screen_rect.h * self.zoom_factor)
                scaled_size = w - w % 2, h - h % 2
                self.surface = pygame.transform.scale(self.orig_surface,
                                                      scaled_size)
                pos = self.rect.topleft
                self.rect = self.surface.get_rect()
                self.rect.topleft = pos

