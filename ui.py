import pygame
from pygame import SRCALPHA, Surface, font, Vector2
import math

from settings import SCALE, WHITE, BLACK, DAY_TIME, MINUTE, WIDTH


class Ui:
    def __init__(self, screen):
        self.screen = screen


class Text(Ui):
    def __init__(self, screen, font_size, color='white',
                 pos=(0, 0), center_align=False, right_align=False, bottom_align=False, vertical_center_align=False, shade=True):

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
    def __init__(self, screen, font_size, sky):

        self.font = font.Font('assets/fonts/PixelOperator8-Bold.ttf',
                                     font_size * SCALE)
        self.screen = screen
        self.sky = sky

        self.r = 50
        self.add_width = 50
        self.w, self.h = self.r * 2 + self.add_width, self.r * 2 + self.add_width
        self.surface = Surface((self.w, self.h / 2), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 128))
        self.rect = self.surface.get_rect()
        self.rect.topleft = (WIDTH - self.w, 0)
        self.center = self.r + self.add_width / 2, self.r + self.add_width / 2

        self.sun_pos = Vector2(self.center) - Vector2(0, self.r)
        self.moon_pos = Vector2(self.center) + Vector2(0, self.r)

        self.angle = 180

        pos = (self.rect.x + self.rect.w / 2, self.rect.y + self.rect.h + 10)
        self.day_label = Text(screen, 4, 'white', pos, center_align=True, shade=True)
        self.time_label = Text(screen, 4, 'white', (pos[0], pos[1] + 20),
                               center_align=True, shade=True)

    def update(self, dt):
        ratio = 1 - abs((round(self.sky.hour) * 60 + round(self.sky.minute) - 12 * 60) / (12 * 60))
        self.angle = (round(self.sky.hour) * 60 + round(self.sky.minute) - 12 * 60) / (24 * 60) * 360 - 90

        self.update_sun_pos()
        self.update_moon_pos()

        self.surface.fill((0, 0, 0, 128))

        pygame.draw.circle(self.surface, WHITE, self.center, self.r, 2)
        pygame.draw.circle(self.surface, (255, min(255, int(255 * abs(ratio))), 0), self.sun_pos, 12)
        pygame.draw.circle(self.surface, 'white', self.moon_pos, 7)

        self.screen.blit(self.surface, self.rect.topleft)
        pygame.draw.line(self.screen, WHITE, (WIDTH - self.rect.w + 5, self.rect.y + self.rect.h - 2),
                                              (WIDTH - 5, self.rect.y + self.rect.h - 2), 2)

        self.day_label.update(f'Day {self.sky.day}')
        # self.time_label.update(self.sky.time)

    def update_sun_pos(self):
        self.sun_pos.x = self.r * math.cos(math.radians(self.angle)) + self.center[0]
        self.sun_pos.y = self.r * math.sin(math.radians(self.angle)) + self.center[1]

    def update_moon_pos(self):
        self.moon_pos.x = -self.r * math.cos(math.radians(self.angle)) + self.center[0]
        self.moon_pos.y = -self.r * math.sin(math.radians(self.angle)) + self.center[1]
