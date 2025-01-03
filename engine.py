from os import path

from pygame.image import load


class Engine:
    def __init__(self):
        self.images = {
            'grass': self.load_image('grass'),
            'tall_grass': self.load_image('tall_grass'),
            'farmland_0': self.load_image('farmland_0'),
            'farmland_1': self.load_image('farmland_1'),
            'farmland_2': self.load_image('farmland_2'),
            'flower': self.load_image('flower'),
            'house': self.load_image('house'),
            'house_light': self.load_image('house_light'),
            'mine': self.load_image('mine'),
            'pathway': self.load_image('pathway'),
            'stone_1': self.load_image('stone_1'),
            'stone_2': self.load_image('stone_2'),
            'stone_3': self.load_image('stone_3'),
            'tree_0': self.load_image('tree_0'),
            'tree_1': self.load_image('tree_1'),
            'tree_2': self.load_image('tree_2'),
            'windmill_1': self.load_image('windmill_1'),
            'windmill_2': self.load_image('windmill_2'),
            'build_house': self.load_image('build_house'),
            'build_mine': self.load_image('build_mine'),
            'build_windmill': self.load_image('build_windmill')
        }

        self.hover_outline = self.load_image('hover')
        self.pressed_outline = self.load_image('pressed')

        self.cursor_regular = self.load_image('cursor')
        self.cursor_pressed = self.load_image('cursor_pressed')

    def load_image(self, name, alpha=False):
        fullname = path.join("assets/sprites/", name + '.png')

        image = load(fullname)
        image = image.convert() if alpha else image.convert_alpha()

        return image
