import pygame

from load_image import load_image
from sprite import Sprite


class Tile(Sprite):
    def __init__(self, name, image, pos, *group):
        super().__init__(*group)

        self.name = name

        self.default_image = load_image(image)
        self.other_image = load_image('test')
        self.image = self.default_image

        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        # if self.rect.collidepoint(mouse_pos):
        #     self.image = self.other_image
        # else:
        #     self.image = self.default_image
