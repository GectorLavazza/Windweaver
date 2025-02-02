import random

import pygame
from pygame import Vector2

from load_image import load_image
from settings import SCALE, WIDTH, HEIGHT
from pygame.sprite import Sprite


class Particle(Sprite):
    def __init__(self, pos, dx, dy, particles, time, *group):
        super().__init__(*group)
        self.particles = particles
        self.image = random.choice(self.particles)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.center = pos

        self.elapsed_time = 0
        self.time = time

        self.base_pos = Vector2(pos)

    def update(self, dt):
        self.rect.x += self.velocity[0] * dt * SCALE
        self.rect.y += self.velocity[1] * dt * SCALE

        self.elapsed_time += dt

        if self.elapsed_time >= self.time:
            self.kill()


        if not (-20 <= self.rect.centerx <= WIDTH + 20 and
                -20 <= self.rect.centery <= HEIGHT + 20):
            self.kill()


def create_particles(color, position, amount, time, *group):
    s = pygame.Surface((1 * SCALE, 1 * SCALE))
    s.fill(color)
    particles = [s]
    for scale in (1.25, 1.5):
        particles.append(pygame.transform.scale_by(particles[0], scale))

    for _ in range(amount):
        dx = random.randint(-50, 50) / 100
        dy = random.randint(-50, 50) / 100
        t = random.randint(max(1, time // 4 * 3), max(2, time // 4 * 5))
        Particle(position, dx, dy, particles, t, *group)
