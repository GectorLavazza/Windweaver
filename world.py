import pygame
from pygame import Vector2

from settings import *


class World:
    def __init__(self, screen: pygame.surface.Surface, size, center, sky):

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.surface = pygame.surface.Surface(size, pygame.SRCALPHA)

        self.rect = self.surface.get_rect()
        self.rect.center = center

        self.speed = 3
        self.edge_threshold = screen_height // 4

        self.dx = 0
        self.dy = 0
        self.dynamic_speed_x = 0
        self.dynamic_speed_y = 0
        self.velocity = pygame.Vector2(0, 0)

        self.wood = 0
        self.stone = 0
        self.food = 0

        self.current_build = 'house'

        self.house_placed = False

        self.houses = 0
        self.mines = 0

        self.sky = sky

        self.visible_rect = pygame.Rect(0, 0, self.screen.get_width(),
                                   self.screen.get_height())
        self.visible_rect = self.visible_rect.clip(self.surface.get_rect())


    def blit(self, surface, dest):
        self.surface.blit(surface, dest)

    def update(self, dt):
        if self.check_mouse_edges():
            self.move(dt)

        self.screen.blit(self.surface, (0, 0), self.visible_rect)


    def check_mouse_edges(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

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

        if self.dx or self.dy:
            return True

    def move(self, dt):
        input_direction = pygame.Vector2(self.dx, self.dy)
        if input_direction.length() > 0:
            input_direction = input_direction.normalize()

        speed_multiplier_x = max(0,
                                 min(1, self.dynamic_speed_x))
        speed_multiplier_y = max(0,
                                 min(1, self.dynamic_speed_y))

        self.velocity.x = input_direction.x * self.speed * speed_multiplier_x * dt
        self.velocity.y = input_direction.y * self.speed * speed_multiplier_y * dt

        if self.velocity.length() > self.speed:
            self.velocity = self.velocity.normalize() * self.speed

        self.rect.x += self.velocity.x * SCALE
        self.rect.y += self.velocity.y * SCALE

        self.rect.x = max(screen_width - self.rect.width,
                          min(self.rect.x, 0))
        self.rect.y = max(screen_height - self.rect.height,
                          min(self.rect.y, 0))

        self.visible_rect.topleft = -Vector2(self.rect.topleft)
