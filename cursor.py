import pygame
from pygame.sprite import Sprite

from engine import Engine

class Cursor(Sprite):
    def __init__(self, engine, *group):
        super().__init__(*group)

        self.regular_image = engine.load_image('cursor')
        self.pressed_image = engine.load_image('cursor_pressed')
        self.image = self.regular_image

        self.pressed = False
        self.rect = self.image.get_rect()

    def update(self, render=True):
        mouse_pos = pygame.mouse.get_pos()
        mouse_focus = pygame.mouse.get_focused()

        if self.pressed:
            self.image = self.pressed_image
        else:
            self.image = self.regular_image

        if mouse_focus:
            self.rect.topleft = mouse_pos
        else:
            self.rect.topleft = (-100, -100)
