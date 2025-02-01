from pygame import SRCALPHA, Surface, freetype

from settings import SCALE


class Ui:
    def __init__(self, screen):
        self.screen = screen


class Text(Ui):
    def __init__(self, screen, font_size, color='white',
                 pos=(0, 0), center_align=False, right_align=False, bottom_align=False, vertical_center_align=False, shade=True):

        super().__init__(screen)
        self.font = freetype.Font('assets/fonts/PixelOperator8-Bold.ttf',
                                     font_size * SCALE)
        self.pos = pos
        self.color = color
        self.center_align = center_align
        self.right_align = right_align
        self.bottom_align = bottom_align
        self.vertical_center_align = vertical_center_align

        self.rect = self.font.get_rect('')
        self.rect.center = self.screen.get_rect().center
        self.font.render_to(self.screen, self.rect.topleft, '', self.color)

        self.prev = ''

        self.shade = Surface(self.rect.size, SRCALPHA)
        self.shade.set_alpha(128)
        self.shade.fill('black')

        self.show_shade = shade

    def update(self, message):

        if message != self.prev:
            self.rect = self.font.get_rect(message)
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

        self.font.render_to(self.screen, self.rect.topleft, message, self.color)

        self.prev = message
