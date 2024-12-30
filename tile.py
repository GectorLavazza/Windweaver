import pygame
import random

from light import Light
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

        self.center = self.pos[0] + self.rect.w // 2, self.pos[1] + self.rect.h // 2

        self.collision_rect = pygame.rect.Rect(*self.rect.topleft,
                                               self.rect.width * 2, self.rect.height * 2)
        self.collision_rect.center = self.rect.center

        self.clicked = False
        self.available = False

        self.colliding = []

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

    def get_colliding(self):
        self.colliding.clear()
        for other in self.groups()[0]:
            if self.collision_rect.colliderect(other.rect):
                if other != self:
                    self.colliding.append(other)

    def handle_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):

            self.check_build_availability()

            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:

                if not self.clicked:
                    self.on_click()
                    self.clicked = True

                self.default_image, self.hover_image, self.pressed_image = self.get_images(
                    self.name)

                self.image = self.pressed_image
            else:
                self.clicked = False
        else:
            self.clicked = False
            self.image = self.default_image

    def move(self):
        self.rect.topleft = (self.pos[0] + self.world.rect.x,
                             self.pos[1] + self.world.rect.y)
        self.collision_rect.center = self.rect.center

    def check_build_availability(self):
        self.get_colliding()
        check = [n.name == 'grass' for n in self.colliding]
        if all(check) and self.name == 'grass':
            self.available = True
        else:
            self.available = False

        if self.available:
            self.image = load_image('test2')
        else:
            self.image = self.hover_image


class Tree(Tile):
    def __init__(self, pos, world, age, *group):
        super().__init__(f'tree_{age}', pos, world, *group)
        self.max_tick = random.randint(60, 7200)
        self.tick = self.max_tick
        self.durability = random.randint(1, 3) + 2 + age
        self.age = age

    def on_click(self):
        self.durability -= 1
        if self.durability <= 0:
            self.on_kill()

    def on_kill(self):
        Grass('grass', self.pos, self.world, self.groups())

        self.world.wood += self.age + 1
        self.kill()

    def grow(self):
        trees_2_count = 0
        trees_1_count = 0
        trees_0_count = 0
        grow = True

        self.get_colliding()
        for other in self.colliding:

            if other.name == 'tree_2':
                trees_2_count += 1
            elif other.name == 'tree_1':
                trees_2_count += 1
            elif other.name == 'tree_0':
                trees_2_count += 1

            if trees_2_count > 2:
                grow = False
                break
            elif trees_1_count + trees_2_count > 2 and self.age == 0:
                grow = False
                break

        if grow:
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
                self.max_tick = random.randint(60, 7200)
                self.tick = self.max_tick
                if random.randint(1, 10) == 1:
                    self.grow()


class Stone(Tile):
    def __init__(self, pos, world, amount, *group):
        super().__init__(f'stone_{amount}', pos, world, *group)
        self.amount = amount
        self.durability = random.randint(1, 2) + self.amount

    def on_click(self):
        self.durability -= 1
        if self.durability <= 0:
            self.on_kill()

    def on_kill(self):
        Grass('grass', self.pos, self.world, self.groups())
        self.world.stone += self.amount
        self.kill()


class House(Tile):
    def __init__(self, pos, world, *group):
        super().__init__('house', pos, world, *group)
        self.lighting = False
        self.light = Light(8, self.center, (255, 200, 0), 0.3, self.world, self.world.light_g)
        self.on = 0
        self.started = False

    def on_update(self, dt):
        self.default_image, self.hover_image, self.pressed_image = self.get_images(
            'house')
        if self.world.sky.dark:
            self.lighting = True
        else:
            self.started = False
            self.lighting = False
            self.light.image.set_alpha(0)

        if self.lighting:
            if not self.started:
                self.on = random.randint(10, 120)
                self.started = True
            else:
                self.on -= dt
                if self.on < 0:
                    self.default_image, self.hover_image, self.pressed_image = self.get_images(
                        'house_light')
                    self.light.image.set_alpha(self.light.density * 255)
        else:
            self.light.image.set_alpha(0)



class Grass(Tile):
    def __init__(self, name, pos, world, *group):
        super().__init__(name, pos, world, *group)
        self.max_tick = random.randint(60, 7200)
        self.tick = self.max_tick

    def grow(self):
        self.name = 'tall_grass'

        tall_grass_count = 0
        trees_count = 0
        flowers_count = 0

        self.get_colliding()
        for other in self.colliding:

            if other.name == 'tall_grass':
                tall_grass_count += 1
            elif 'tree' in other.name:
                trees_count += 1
            elif other.name == 'flower':
                flowers_count += 1

            if trees_count > 5:
                Tree(self.pos, self.world, 0, self.groups())
                self.kill()
                break
            elif trees_count > 2:
                if random.randint(1, 10) == 1:
                    Tree(self.pos, self.world, 0, self.groups())
                    self.kill()
                break
            elif flowers_count > 2:
                if random.randint(1, 10) == 1:
                    self.name = 'flower'
                break
            elif tall_grass_count > 5:
                self.name = 'tall_grass'
                break

        self.default_image, self.hover_image, self.pressed_image = self.get_images(
            self.name)
        self.image = self.default_image

    def on_click(self):
        if self.available:
            House(self.pos, self.world, self.groups())
            self.kill()

        self.name = 'grass'

        self.default_image, self.hover_image, self.pressed_image = self.get_images(
            self.name)
        self.image = self.default_image

        self.max_tick = random.randint(60, 7200)
        self.tick = self.max_tick

    def on_update(self, dt):
        if self.name not in ('tall_grass', 'flower'):
            self.tick -= 1 * dt
            if self.tick <= 0:
                self.max_tick = random.randint(60, 7200)
                self.tick = self.max_tick
                if random.randint(1, 5) == 1:
                    self.grow()
