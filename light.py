import pygame

from settings import SCALE


class Light:
    def __init__(self, surface, radius, color, density):
        self.surface = surface

        self.color = color
        self.density = density

        self.r = radius * SCALE
        self.w = self.h = self.r * 2

        self.image = self.get_image()
        self.rect = self.image.get_rect()

    def update(self):
        self.surface.blit(self.image, self.rect.topleft, special_flags=pygame.BLEND_RGB_ADD)

    def get_image(self):
        image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        image.set_colorkey((0, 0, 0))

        for i in range(self.density):
            radius = (self.r - self.r / 10 * (self.density - i))

            surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            pygame.draw.circle(surface, self.color, (self.r, self.r), radius)

            image.blit(surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

        return image
