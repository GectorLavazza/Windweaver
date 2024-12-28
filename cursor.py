import pygame

from load_image import load_image
from sprite import Sprite


class Cursor(Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image('cursor', True)
        self.rect = self.image.get_rect()

    def update(self, render=True):
        mouse_pos = pygame.mouse.get_pos()
        mouseFocus = pygame.mouse.get_focused()

        if mouseFocus:
            self.rect.topleft = mouse_pos
        else:
            self.rect.topleft = (-100, -100)
