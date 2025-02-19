import pygame
from pygame import Surface

from settings import screen_size, DAY_TIME, HOUR, MINUTE


class Sky:
    def __init__(self, screen):
        self.screen = screen

        self.day = 0
        self.time = ''
        self.hour = 0
        self.minute = 0

        self.phases = ['day', 'sunset', 'night', 'sunrise']
        self.current_phase = 2

        self.tick = DAY_TIME // 4 * self.current_phase

        self.surface = Surface(screen_size, pygame.SRCALPHA)

        self.orange_surface = Surface(screen_size, pygame.SRCALPHA)
        self.orange_surface.fill((255, 102, 0))

        self.black_surface = Surface(screen_size, pygame.SRCALPHA)
        self.black_surface.fill('black')

    def calculate_time(self):
        self.hour = self.tick // HOUR + 1
        self.minute = (self.tick - (self.hour - 1) * HOUR) // MINUTE
        f = 'AM' if 0 <= round(self.hour) < 13 else 'PM'
        h = round(self.hour) if f == 'AM' else round(self.hour) - 12
        self.time = (f'{str(round(h)).rjust(2, "0")}:'
                     f'{str(round(self.minute)).rjust(2, "0")} {f}')

    def update(self, dt):

        self.tick += dt
        if self.tick >= DAY_TIME:
            self.current_phase = max(0, min(self.current_phase + 1, 3))
            self.tick = 0
            self.day += 1

        self.calculate_time()

        self.surface.fill((0, 0, 0, 0))
        # self.surface.blit(self.orange_surface, (0, 0))
        # self.surface.blit(self.black_surface, (0, 0))
        self.screen.blit(self.surface, (0, 0))
