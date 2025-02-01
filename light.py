import pygame
from pygame.sprite import Sprite
from settings import SCALE, WIDTH, HEIGHT, screen_size


class Light(Sprite):
    def __init__(self, radius, pos, color, density, world, *group):
        super().__init__(*group)

        self.color = color
        self.density = density
        self.world = world

        self.r = radius * SCALE
        self.w = self.h = self.r * 2

        self.image = self.get_image()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = self.rect.topleft

    def update(self, dt):
        self.rect.topleft = (self.pos[0] + self.world.rect.x,
                             self.pos[1] + self.world.rect.y)
        self.world.screen.blit(self.image, self.rect.topleft)
        self.enlight(self.world.sky.surface)

    def get_image(self):
        image = pygame.Surface((self.w, self.h)).convert_alpha()

        image.set_alpha(255)
        image.fill(pygame.Color(0, 0, 0, 0))

        for i in range(4):
            ck = self.density / 4 * (i + 1)
            color = pygame.Color(*self.color, int(255 * ck))
            radius = int(self.r / 4 * (4 - i))
            pygame.draw.circle(image, color, (self.r, self.r), radius)

        return image

    def enlight(self, surface):
        color = pygame.Color(0, 0, 0, 0)
        center = self.rect.center
        pygame.draw.circle(surface, color, center, self.r * 2)
