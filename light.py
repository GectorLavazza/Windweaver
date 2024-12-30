import pygame
from sprite import Sprite
from settings import SCALE, screen_width, screen_height


class Light(Sprite):
    def __init__(self, radius, pos, color, density, darkness,  *group):
        super().__init__(*group)

        self.color = color
        self.density = density

        self.darkness = darkness

        self.r = radius
        self.w = self.h = self.r * 2

        self.image = self.get_image()
        self.rect = self.image.get_rect()
        self.rect.center = pos[0] * SCALE, pos[1] * SCALE

        self.enlight()

        self.max_playback = 30
        self.playback = self.max_playback

    def update(self, dt):
        pass

    def get_image(self):
        image = pygame.Surface((self.w, self.h)).convert_alpha()

        image.set_alpha(255)
        image.fill(pygame.Color(0, 0, 0, 0))

        for i in range(4):
            ck = self.density / 4 * (i + 1)
            color = pygame.Color(*self.color, int(255 * ck))
            radius = int(self.r / 4 * (4 - i))
            pygame.draw.circle(image, color, (self.r, self.r), radius)
        image = pygame.transform.scale_by(image, SCALE)

        return image

    def enlight(self):
        color = pygame.Color(0, 0, 0, 0)
        center = self.rect.center
        radius = self.r * SCALE * 1.2
        pygame.draw.circle(self.darkness.surface, color, center, radius)


class Darkness:
    def __init__(self):
        self.surface = pygame.Surface((screen_width, screen_height)).convert_alpha()
        self.surface.set_alpha(70)
        self.surface.fill(pygame.Color(0, 0, 0))

    def draw(self, screen):
        screen.blit(self.surface, (0, 0))
