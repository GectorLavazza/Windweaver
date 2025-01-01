import os

import pygame
from settings import SCALE


def load_image(name):
    fullname = os.path.join("assets/sprites/", name + '.png')

    try:
        image = pygame.image.load(fullname).convert_alpha()
        image = pygame.transform.scale_by(image, SCALE).convert_alpha()

    except pygame.error as e:
        print(f"Err: {e}")
        raise SystemExit(e)

    return image
