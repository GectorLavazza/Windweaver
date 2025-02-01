from os import path

from pygame import transform
from pygame.image import load

from settings import SCALE


def load_image(name, alpha=False):
    fullname = path.join("assets/sprites/", name + '.png')

    image = load(fullname)
    image = image.convert() if alpha else image.convert_alpha()

    image = transform.scale_by(image, SCALE)

    return image
