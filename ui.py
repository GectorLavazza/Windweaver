from pygame.font import Font
from pygame.transform import scale
from pygame import SRCALPHA, Surface, freetype

from settings import screen_height, screen_width, SCALE


class Ui:
    def __init__(self, screen):
        self.screen = screen


class Text(Ui):
    def __init__(self, screen, font_size, color='white',
                 pos=(0, 0), center_align=False, right_align=False):

        super().__init__(screen)
        self.font = freetype.Font('assets/fonts/PixelOperator8-Bold.ttf',
                                     font_size * SCALE)
        self.pos = pos
        self.color = color
        self.center_align = center_align
        self.right_align = right_align

        self.rect = self.font.get_rect('')
        self.rect.center = self.screen.get_rect().center
        self.font.render_to(self.screen, self.rect.topleft, '', self.color)

        self.prev = ''

        self.shade = Surface(self.rect.size, SRCALPHA)
        self.shade.set_alpha(128)
        self.shade.fill('black')

    def update(self, message):

        if message != self.prev:
            self.rect = self.font.get_rect(message)
            self.rect.center = self.screen.get_rect().center

            self.shade = Surface(self.rect.size, SRCALPHA)
            self.shade.set_alpha(128)
            self.shade.fill('black')

            if self.center_align:
                self.rect.topleft = (self.pos[0] - self.rect.w // 2,
                       self.pos[1])
            elif self.right_align:
                self.rect.topleft = (self.pos[0] - self.rect.w,
                       self.pos[1])
            else:
                self.rect.topleft = (self.pos[0] * SCALE,
                       self.pos[1])

        self.screen.blit(self.shade, self.rect.topleft)

        self.font.render_to(self.screen, self.rect.topleft, message, self.color)

        self.prev = message
