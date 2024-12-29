import pygame
from settings import *


class Surface:
    def __init__(self, screen: pygame.surface.Surface, size, center):

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.surface = pygame.surface.Surface(size, pygame.SRCALPHA)
        self.size = size

        self.rect = self.surface.get_rect()
        self.rect.center = center
        self.pos = self.rect.topleft

        self.center = center

        self.speed = 3
        self.edge_threshold = screen_height // 4

        self.dx = 0
        self.dy = 0
        self.dynamic_speed_x = 0
        self.dynamic_speed_y = 0
        self.velocity = pygame.Vector2(0, 0)

    def update(self, dt):
        self.screen.blit(self.surface, self.pos)
        self.check_mouse_edges()
        self.move(dt)

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

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        self.rect.x = max(self.screen_rect.width - self.rect.width,
                          min(self.rect.x, 0))
        self.rect.y = max(self.screen_rect.height - self.rect.height,
                          min(self.rect.y, 0))

        self.pos = self.rect.topleft