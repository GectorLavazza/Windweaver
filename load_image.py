import os

import pygame
from settings import SCALE

def load_image(name, scale=False):
    fullname = os.path.join("assets/sprites/", name + '.png')

    try:
        image = pygame.image.load(fullname).convert_alpha()
        if scale:
            image = pygame.transform.scale_by(image, SCALE)

    except pygame.error as e:
        print(f"Err: {e}")
        raise SystemExit(e)

    return image
