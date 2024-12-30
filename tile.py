import pygame
import random

from load_image import load_image
from sprite import Sprite


class Tile(Sprite):
    def __init__(self, name, pos, world, *group):
        super().__init__(*group)
        self.world = world

        self.name = name

        self.default_image, self.hover_image, self.pressed_image = self.get_images(
            self.name)
        self.image = self.default_image

        self.pos = pos

        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] + self.world.rect.x,
                             pos[1] + self.world.rect.y)

        self.collision_rect = self.rect.scale_by(1.1, 1.1)
        self.collision_rect.center = self.rect.center

        self.clicked = False

    def get_images(self, image):
        default = load_image(image)

        hover_outline = load_image('hover')
        pressed_outline = load_image('pressed')

        hover = default.copy()
        pressed = default.copy()

        hover.blit(hover_outline, (0, 0))
        pressed.blit(pressed_outline, (0, 0))

        return default, hover, pressed

    def update(self, dt):
        self.move()
        self.handle_mouse()
        self.on_update(dt)

    def on_update(self, dt):
        pass

    def on_click(self):
        pass

    def on_kill(self):
        pass

    def handle_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:

                if not self.clicked:
                    self.on_click()
                    self.clicked = True

                self.default_image, self.hover_image, self.pressed_image = self.get_images(
                    self.name)

                self.image = self.pressed_image
            else:
                self.clicked = False
                self.image = self.hover_image
        else:
            self.clicked = False
            self.image = self.default_image

    def move(self):
        self.rect.topleft = (self.pos[0] + self.world.rect.x,
                             self.pos[1] + self.world.rect.y)


class Tree(Tile):
    def __init__(self, pos, world, age, *group):
        super().__init__(f'tree_{age}', pos, world, *group)
        self.max_tick = random.randint(60, 36000)
        self.tick = self.max_tick
        self.durability = random.randint(2, 5) + 2 * age
        self.age = age

    def on_click(self):
        self.durability -= 1
        if self.durability <= 0:
            self.on_kill()

    def on_kill(self):
        if random.randint(1, 10) == 1:
            Tile('house', self.pos, self.world, self.groups())
        else:
            Grass('grass', self.pos, self.world, self.groups())

        self.kill()

    def grow(self):
        self.age += 1
        self.durability = random.randint(2, 5) + 2 * self.age

        self.name = f'tree_{self.age}'

        self.default_image, self.hover_image, self.pressed_image = self.get_images(
            self.name)
        self.image = self.default_image

    def on_update(self, dt):
        if self.age < 2:
            self.tick -= 1 * dt
            if self.tick <= 0:
                self.tick = self.max_tick
                self.grow()


class Stones(Tile):
    def __init__(self, pos, world, *group):
        super().__init__('stones', pos, world, *group)
        self.durability = random.randint(2, 4)

    def on_click(self):
        self.durability -= 1
        if self.durability <= 0:
            self.on_kill()

    def on_kill(self):
        Grass('grass', self.pos, self.world, self.groups())
        self.kill()


class Grass(Tile):
    def __init__(self, name, pos, world, *group):
        super().__init__(name, pos, world, *group)
        self.max_tick = random.randint(60, 36000)
        self.tick = self.max_tick

    def grow(self):
        self.name = 'tall_grass'

        tall_grass_count = 0
        stones_count = 0
        trees_count = 0
        flowers_count = 0

        for other in self.groups()[0]:
            if self.collision_rect.colliderect(other.rect):

                if other.name == 'tall_grass':
                    tall_grass_count += 1
                elif 'tree' in other.name:
                    trees_count += 1
                elif other.name == 'stone':
                    stones_count += 1
                elif other.name == 'flower':
                    flowers_count += 1

                if trees_count > 2:
                    if random.randint(1, 10) == 1:
                        Tree(self.pos, self.world, 0, self.groups())
                        self.kill()
                    break
                elif tall_grass_count >= 4 and stones_count == 0 or flowers_count > 2:
                    if random.randint(1, 10) == 1:
                        self.name = 'flower'
                    break

        self.default_image, self.hover_image, self.pressed_image = self.get_images(
            self.name)
        self.image = self.default_image

    def on_click(self):
        self.name = 'grass'

        self.default_image, self.hover_image, self.pressed_image = self.get_images(
            self.name)
        self.image = self.default_image

        self.max_tick = random.randint(60, 36000)
        self.tick = self.max_tick

    def on_update(self, dt):
        if self.name not in ('tall_grass', 'flower'):
            self.tick -= 1 * dt
            if self.tick <= 0:
                self.tick = self.max_tick
                self.grow()
