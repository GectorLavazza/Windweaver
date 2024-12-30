import pygame
from sprite import Sprite
from settings import SCALE, screen_size


class Light(Sprite):
    def __init__(self, radius, pos, color, density, world, *group):
        super().__init__(*group)

        self.color = color
        self.density = density

        self.world = world

        self.r = radius
        self.w = self.h = self.r * 2

        self.pos = pos

        self.image = self.get_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos[0] + self.world.rect.x - self.rect.w // 2,
                             self.pos[1] + self.world.rect.y - self.rect.h // 2)

        self.max_playback = 30
        self.playback = self.max_playback

    def update(self, dt):
        self.rect.topleft = (
        self.pos[0] + self.world.rect.x - self.rect.w // 2,
        self.pos[1] + self.world.rect.y - self.rect.h // 2)

    def get_image(self):
        image = pygame.Surface((self.w, self.h)).convert_alpha()

        image.set_alpha(255)
        image.fill(pygame.Color(0, 0, 0, 0))

        # for i in range(4):
        #     ck = self.density / 4 * (i + 1)
        #     color = (*self.color, int(255 * ck))
        #     radius = int(self.r / 4 * (4 - i))
        #     pygame.draw.circle(image, color, (self.r, self.r), radius)
        color = (*self.color, int(255 * self.density))
        pygame.draw.circle(image, color, (self.r, self.r), self.r)

        image = pygame.transform.scale_by(image, SCALE)

        return image

    def enlight(self, surface):
        color = pygame.Color(0, 0, 0, 0)
        center = self.rect.center
        radius = self.r * SCALE * 100
        pygame.draw.circle(surface, color, center, radius)
