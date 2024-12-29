import pygame

from load_image import load_image
from settings import SCALE
from sprite import Sprite


class Tile(Sprite):
    def __init__(self, name, pos, *group):
        super().__init__(*group)

        self.name = name

        self.default_image = load_image(name)
        self.other_image = load_image('test')
        self.image = self.default_image

        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self, screen, dt):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.other_image
            print(self.rect)
            pygame.draw.rect(screen, 'red', self.rect)
        else:
            self.image = self.default_image
