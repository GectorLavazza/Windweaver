import pygame
from pygame import SRCALPHA, Surface, font, Vector2
import math

from settings import *


class Ui:
    def __init__(self, screen):
        self.screen = screen


class Text(Ui):
    def __init__(self, screen, font_size, color='white',
                 pos=(0, 0), center_align=False, right_align=False, bottom_align=False, vertical_center_align=False, shade=False):

        super().__init__(screen)
        self.font = font.Font('assets/fonts/PixelOperator8-Bold.ttf',
                                     font_size * SCALE)
        self.pos = pos
        self.color = color
        self.center_align = center_align
        self.right_align = right_align
        self.bottom_align = bottom_align
        self.vertical_center_align = vertical_center_align

        self.render = self.font.render('', True, self.color)

        self.rect = self.render.get_rect()
        self.rect.center = self.screen.get_rect().center

        self.prev = ''

        self.shade = Surface(self.rect.size, SRCALPHA)
        self.shade.set_alpha(128)
        self.shade.fill('black')

        self.show_shade = shade

    def update(self, message):

        if message != self.prev:
            self.render = self.font.render(str(message), True,
                                           self.color)
            self.rect = self.render.get_rect()
            self.rect.center = self.screen.get_rect().center

            self.shade = Surface(self.rect.size, SRCALPHA)
            self.shade.set_alpha(128)
            self.shade.fill('black')

            x, y = self.pos
            if self.center_align:
                x = self.pos[0] - self.rect.w // 2
            if self.vertical_center_align:
                y = self.pos[1] - self.rect.h // 2
            if self.right_align:
                x = self.pos[0] - self.rect.w
            if self.bottom_align:
                y = self.pos[1] - self.rect.h

            self.rect.topleft = x, y

        if self.show_shade:
            self.screen.blit(self.shade, self.rect.topleft)

        self.screen.blit(self.render, self.rect.topleft)

        self.prev = message


class Clock:
    def __init__(self, screen, font_size, sky, world):

        self.font = font.Font('assets/fonts/PixelOperator8-Bold.ttf',
                                     font_size * SCALE)
        self.screen = screen
        self.sky = sky

        self.sun = world.images['sun']
        self.moon = world.images['moon']
        self.sun_rect = self.sun.get_rect()
        self.moon_rect = self.moon.get_rect()

        self.r = 10 * SCALE
        self.add_width = 10 * SCALE
        self.w, self.h = self.r * 2 + self.add_width, self.r * 2 + self.add_width

        self.surface = Surface((self.w, self.h / 2), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))

        self.rect = self.surface.get_rect()
        self.rect.topleft = (WIDTH - self.w, 0)
        self.center = self.r + self.add_width / 2, self.r + self.add_width / 2

        self.angle = 180

        pos = (self.rect.x + self.rect.w / 2, self.rect.y + self.rect.h - 5 * SCALE)
        self.day_label = Text(screen, 4, 'white', pos, center_align=True, shade=False)
        # self.time_label = Text(screen, 4, 'white', (pos[0], pos[1] + 20),
        #                        center_align=True, shade=True)

    def update(self, dt):
        self.angle = (round(self.sky.hour) * 60 + round(self.sky.minute) - 12 * 60) / (24 * 60) * 360 - 90

        self.update_sun_pos()
        self.update_moon_pos()

        self.surface.fill((0, 0, 0, 0))

        pygame.draw.circle(self.surface, WHITE, self.center, self.r, 1 + SCALE // 2)
        self.surface.blit(self.sun, self.sun_rect.topleft)
        self.surface.blit(self.moon, self.moon_rect.topleft)

        self.screen.blit(self.surface, self.rect.topleft)
        pygame.draw.line(self.screen, WHITE, (WIDTH - self.rect.w + SCALE, self.rect.y + self.rect.h),
                                              (WIDTH - SCALE, self.rect.y + self.rect.h), 1 + SCALE // 2)

        self.day_label.update(f'{self.sky.day}')
        # self.time_label.update(self.sky.time)

    def update_sun_pos(self):
        self.sun_rect.centerx = self.r * math.cos(math.radians(self.angle)) + self.center[0]
        self.sun_rect.centery = self.r * math.sin(math.radians(self.angle)) + self.center[1]

    def update_moon_pos(self):
        self.moon_rect.centerx = -self.r * math.cos(math.radians(self.angle)) + self.center[0]
        self.moon_rect.centery = -self.r * math.sin(math.radians(self.angle)) + self.center[1]


class Resources:
    def __init__(self, screen, world):
        self.screen = screen
        self.world = world
        self.pos = (0, 0)

        self.w, self.h = 50 * SCALE, 20 * SCALE
        self.surface = Surface((self.w, self.h), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        self.rect = self.surface.get_rect()

        self.text = Surface((self.w, self.h), pygame.SRCALPHA)
        self.text.fill((0, 0, 0, 0))

        self.back = Surface((self.w, self.h), pygame.SRCALPHA)
        self.back.fill((0, 0, 0, 0))

        self.rw, self.rh = 30 * SCALE, 4 * SCALE
        self.wood_w = self.rw
        self.stone_w = self.rw

        pygame.draw.rect(self.back, DARK_GREY, pygame.Rect(8 * SCALE - SCALE, 3 * SCALE + SCALE, self.rw, self.rh))
        pygame.draw.rect(self.back, DARK_GREY, pygame.Rect(8 * SCALE - SCALE, 3 * SCALE + self.rh * 0.5 * SCALE + SCALE, self.rw, self.rh))

        self.wood_count = Text(self.text, 4, BLACK, (8 * SCALE + self.rw / 2, 3.5 * SCALE + self.rh / 2), center_align=True, vertical_center_align=True)
        self.stone_count = Text(self.text, 4, BLACK, (8 * SCALE + self.rw / 2, 3.5 * SCALE + self.rh / 2 + self.rh * 0.5 * SCALE), center_align=True, vertical_center_align=True)

        self.stone = self.world.images['stone_icon']
        self.wood = self.world.images['wood_icon']

        self.text_alpha = 0

    def update(self, dt):
        self.surface.fill((0, 0, 0, 0))
        self.text.fill((0, 0, 0, 0))
        self.text.set_alpha(self.text_alpha)
        self.surface.blit(self.back, (0, 0))

        self.wood_w = max(self.wood_w - dt * STATS_BAR_SPEED,
            min(self.wood_w + dt * STATS_BAR_SPEED, self.rw / self.world.max_wood * self.world.wood))
        self.stone_w = max(self.stone_w - dt * STATS_BAR_SPEED,
                          min(self.stone_w + dt * STATS_BAR_SPEED, self.rw / self.world.max_stone * self.world.stone))

        pygame.draw.rect(self.surface, WHITE, pygame.Rect(8 * SCALE, 3 * SCALE, self.wood_w, self.rh))
        pygame.draw.rect(self.surface, WHITE, pygame.Rect(8 * SCALE, 3 * SCALE + self.rh * 0.5 * SCALE, self.stone_w, self.rh))

        self.surface.blit(self.wood, (2 * SCALE, 5 * SCALE - 3 * SCALE))
        self.surface.blit(self.stone, (2 * SCALE, 5 * SCALE + self.rh * 0.5 * SCALE - 3 * SCALE))

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.text_alpha = min(int(self.text_alpha + dt * STATS_ALPHA_SPEED), 255)
        else:
            self.text_alpha = max(int(self.text_alpha - dt * STATS_ALPHA_SPEED), 0)

        self.screen.blit(self.surface, self.pos)

        if self.text_alpha >= 0:
            self.wood_count.update(f'{self.world.wood}/{self.world.max_wood}')
            self.stone_count.update(f'{self.world.stone}/{self.world.max_stone}')
            self.screen.blit(self.text, self.pos)
