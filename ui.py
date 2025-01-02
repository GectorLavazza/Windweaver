from pygame.font import Font
from pygame.transform import scale
from pygame import SRCALPHA, Surface

from settings import screen_height, screen_width


class Ui:
    def __init__(self, screen):
        self.screen = screen


class Text(Ui):
    def __init__(self, screen, font_size, color='white',
                 pos=(0, 0), center_align=False, right_align=False):

        super().__init__(screen)
        self.font = Font('assets/fonts/PixelOperator8-Bold.ttf',
                                     font_size)
        self.pos = pos
        self.color = color
        self.center_align = center_align
        self.right_align = right_align

        self.render = self.font.render('', True, self.color).convert_alpha()
        self.rect = self.render.get_rect()

        self.prev = ''

        self.shade = Surface(self.rect.size, SRCALPHA)
        self.shade.set_alpha(128)
        self.shade.fill('black')

    def update(self, message):

        if message != self.prev:
            self.render = self.font.render(str(message), True,
                                           self.color).convert_alpha()
            self.rect = self.render.get_rect()

            if self.center_align:
                self.rect.topleft = (self.pos[0] - self.render.get_width() // 2,
                       self.pos[1])
            elif self.right_align:
                self.rect.topleft = (self.pos[0] - self.render.get_width(),
                       self.pos[1])
            else:
                self.rect.topleft = (self.pos[0],
                       self.pos[1])

            self.shade = scale(self.shade, self.rect.size)

        self.screen.blit(self.shade, self.rect.topleft)
        self.screen.blit(self.render, self.rect.topleft)

        self.prev = message
