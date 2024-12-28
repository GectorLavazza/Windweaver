import os

import pygame

def load_image(name):
    fullname = os.path.join("assets/sprites/", name + '.png')

    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as e:
        print(f"Err: {e}")
        raise SystemExit(e)

    return image
