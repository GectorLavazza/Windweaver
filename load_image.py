from os import path

from pygame import transform
from pygame.image import load

from settings import SCALE, PATH


def load_image(name, alpha=False):
    fullname = path.join(PATH, "assets/sprites/", name + '.png')

    image = load(fullname)
    image = image.convert() if alpha else image.convert_alpha()

    image = transform.scale_by(image, SCALE)

    return image
