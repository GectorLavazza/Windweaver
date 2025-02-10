import random

import pygame
from pygame import Vector2
from pygame.sprite import Sprite

from settings import SCALE, WIDTH, HEIGHT


class Particle(Sprite):
    def __init__(self, pos, dx, dy, particles, time, *group):
        super().__init__(*group)
        self.particles = particles
        self.image = random.choice(self.particles)
        self.rect = self.image.get_rect()

        self.velocity = Vector2(dx, dy)
        self.rect.center = pos

        self.elapsed_time = 0
        self.time = time

        self.base_pos = Vector2(pos)

    def update(self, dt):
        self.velocity.x += random.randint(-100, 100) / 1000
        self.velocity.y += random.randint(-100, 100) / 1000

        self.rect.x += self.velocity.x * dt * SCALE
        self.rect.y += self.velocity.y * dt * SCALE

        self.elapsed_time += dt

        self.image.set_alpha(int(255 * (1 - self.elapsed_time / 1.25 / self.time)))

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
        dx = random.randint(-500, 500) / 1000
        dy = random.randint(-500, 500) / 1000
        t = random.randint(max(1, time // 4 * 3), max(2, time // 4 * 5))
        Particle(position, dx, dy, particles, t, *group)
