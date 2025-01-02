from os import path

from pygame.image import load


def load_image(name, alpha=False):
    fullname = path.join("assets/sprites/", name + '.png')

    image = load(fullname)
    image = image.convert() if alpha else image.convert_alpha()

    # image = pygame.transform.scale_by(image, SCALE).convert_alpha()

    return image
