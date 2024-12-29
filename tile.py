import pygame

from load_image import load_image
from sprite import Sprite


class Tile(Sprite):
    def __init__(self, name, pos, world, *group):
        super().__init__(*group)
        self.world = world

        self.name = name

        self.default_image = load_image(name)

        self.default_image, self.hover_image, self.pressed_image = self.get_images(name)
        self.image = self.default_image

        self.pos = pos

        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] + self.world.rect.x,
                             pos[1] + self.world.rect.y)

    def get_images(self, image):
        default = load_image(image)

        hover_outline = load_image('hover')
        pressed_outline = load_image('pressed')

        hover = default.copy()
        pressed = default.copy()

        hover.blit(hover_outline, (0, 0))
        pressed.blit(pressed_outline, (0, 0))

        return default, hover, pressed

    def update(self, dt):
        self.rect.topleft = (self.pos[0] + self.world.rect.x,
                             self.pos[1] + self.world.rect.y)

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                self.name = 'house'
                self.default_image, self.hover_image, self.pressed_image = self.get_images(self.name)

                self.image = self.pressed_image
            else:
                self.image = self.hover_image
        else:
            self.image = self.default_image
