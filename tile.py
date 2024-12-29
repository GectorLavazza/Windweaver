import pygame

from load_image import load_image
from sprite import Sprite


class Tile(Sprite):
    def __init__(self, name, pos, world, *group):
        super().__init__(*group)
        self.world = world

        self.name = name

        self.default_image = load_image(name)
        self.hover_image = load_image('test1')
        self.pressed_image = load_image('test2')
        self.image = self.default_image

        self.pos = pos

        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] + self.world.rect.x,
                             pos[1] + self.world.rect.y)

    def update(self, dt):
        self.rect.topleft = (self.pos[0] + self.world.rect.x,
                             self.pos[1] + self.world.rect.y)

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                self.image = self.pressed_image
            else:
                self.image = self.hover_image
        else:
            self.image = self.default_image
