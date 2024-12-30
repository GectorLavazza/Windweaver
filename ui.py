import pygame

from settings import *

class Ui:
    def __init__(self, screen, screen_size):
        self.screen = screen
        self.width = screen_size[0]
        self.height = screen_size[1]


class Text(Ui):
    def __init__(self, screen, screen_size, font_size, color='white',
                 pos=(0, 0), center_align=False, right_align=False):
        super().__init__(screen, screen_size)
        self.font = pygame.font.Font('assets/fonts/PixelOperator8-Bold.ttf',
                                     int(font_size * SCALE))
        self.pos = pos
        self.color = pygame.Color(color)
        self.center_align = center_align
        self.right_align = right_align

        self.render = self.font.render('', True, self.color).convert_alpha()
        self.rect = self.render.get_rect()

    def update(self, message):
        self.render = self.font.render(str(message), True,
                                       self.color).convert_alpha()
        self.rect = self.render.get_rect()
        if self.center_align:
            pos = (self.pos[0] - self.render.get_width() // 2,
                   self.pos[1] - self.render.get_height() // 2)
        elif self.right_align:
            pos = (self.pos[0] - self.render.get_width(),
                   self.pos[1])
        else:
            pos = (self.pos[0],
                   self.pos[1])
        shade = pygame.surface.Surface(self.rect.size, pygame.SRCALPHA)
        shade.set_alpha(128)
        shade.fill('black')
        self.screen.blit(shade, pos)
        self.screen.blit(self.render, pos)
