import pygame
import random

from pygame.examples.cursors import image

from light import Light
from load_image import load_image
from settings import GROWTH_MIN, GROWTH_MAX, HOUSE_STONE_COST, HOUSE_WOOD_COST, \
    MINE_STONE_COST, MINE_WOOD_COST, SCALE
from sprite import Sprite


class Tile(Sprite):
    def __init__(self, name, pos, world, *group):
        super().__init__(*group)
        self.world = world

        self.name = name
        self.durability = 0
        self.max_durability = self.durability

        self.default_image, self.hover_image, self.pressed_image = self.get_images(
            self.name)
        self.image = self.default_image

        self.pos = pos

        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] + self.world.rect.x,
                             pos[1] + self.world.rect.y)

        self.center = self.pos[0] + self.rect.w // 2, self.pos[
            1] + self.rect.h // 2

        self.collision_rect = pygame.rect.Rect(*self.rect.topleft,
                                               self.rect.width * 2,
                                               self.rect.height * 2)
        self.collision_rect.center = self.rect.center

        self.clicked = False
        self.house_available = False
        self.mine_available = False

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
                    self.colliding.append(other.name)

    def handle_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):

            self.check_house_build()
            self.check_mine_build()

            self.draw_durability_bar(self.world.screen)

            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:

                if not self.clicked:
                    self.on_click()
                    self.clicked = True

                self.default_image, self.hover_image, self.pressed_image = self.get_images(
                    self.name)

                self.image = self.pressed_image
            else:
                self.image = self.hover_image

                if self.house_available:
                    if self.check_house_cost():
                        self.image = load_image('build_house')
                elif self.mine_available:
                    if self.check_mine_cost():
                        self.image = load_image('build_mine')

                self.clicked = False
        else:
            self.clicked = False
            self.image = self.default_image

    def move(self):
        self.rect.topleft = (self.pos[0] + self.world.rect.x,
                             self.pos[1] + self.world.rect.y)
        self.collision_rect.center = self.rect.center

    def check_house_build(self):
        self.get_colliding()
        check = [n in ('grass', 'flower') for n in self.colliding]
        if all(check) and self.name == 'grass':
            self.house_available = True
        else:
            self.house_available = False

    def check_mine_build(self):
        self.get_colliding()
        check = ['stone' in n for n in self.colliding]
        check2 = ['tree' not in n and 'mine' not in n for n in self.colliding]
        if check.count(True) > 2 and all(check2) and self.colliding.count(
                'tall_grass') == 0 and self.name == 'grass':
            if self.world.houses // 2 >= (self.world.mines + 1):
                self.mine_available = True
        else:
            self.mine_available = False

    def check_house_cost(self):
        if self.world.stone - HOUSE_STONE_COST >= 0 and self.world.wood - HOUSE_WOOD_COST >= 0:
            return True

    def buy_house(self):
        self.world.stone -= HOUSE_STONE_COST
        self.world.wood -= HOUSE_WOOD_COST

    def check_mine_cost(self):
        if self.world.stone - MINE_STONE_COST >= 0 and self.world.wood - MINE_WOOD_COST >= 0:
            return True

    def buy_mine(self):
        self.world.stone -= MINE_STONE_COST
        self.world.wood -= MINE_WOOD_COST

    def draw_durability_bar(self, screen):
        w, h = 12, 2
        if self.max_durability:
            pygame.draw.rect(screen, pygame.Color('#46474c'),
                             pygame.Rect(self.rect.centerx - (w // 2 + 1) * SCALE,
                                         self.rect.y - (h - 1) * SCALE,
                                         w * SCALE, h * SCALE))
            pygame.draw.rect(screen, pygame.Color('#e0dca4'),
                             pygame.Rect(self.rect.centerx - (w // 2) * SCALE,
                                         self.rect.y - h * SCALE,
                                         w / self.max_durability * self.durability * SCALE,
                                         h * SCALE))


class Tree(Tile):
    def __init__(self, pos, world, age, *group):
        super().__init__(f'tree_{age}', pos, world, *group)
        self.max_tick = random.randint(GROWTH_MIN, GROWTH_MAX)
        self.tick = self.max_tick
        self.durability = age + 2
        self.max_durability = self.durability
        self.age = age

    def on_click(self):
        if pygame.mouse.get_pressed()[0]:
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

            if other == 'tree_2':
                trees_2_count += 1
            elif other == 'tree_1':
                trees_2_count += 1
            elif other == 'tree_0':
                trees_2_count += 1

            if trees_2_count > 2:
                grow = False
                break
            elif trees_1_count + trees_2_count > 2 and self.age == 0:
                grow = False
                break

        if grow:
            self.age += 1
            self.durability = self.age + 2
            self.max_durability = self.durability

            self.name = f'tree_{self.age}'

            self.default_image, self.hover_image, self.pressed_image = self.get_images(
                self.name)
            self.image = self.default_image

    def on_update(self, dt):
        if self.age < 2:
            self.tick -= 1 * dt
            if self.tick <= 0:
                self.max_tick = random.randint(GROWTH_MIN, GROWTH_MAX)
                self.tick = self.max_tick
                if random.randint(1, 10) == 1:
                    self.grow()


class Stone(Tile):
    def __init__(self, pos, world, amount, *group):
        super().__init__(f'stone_{amount}', pos, world, *group)
        self.amount = amount
        self.durability = self.amount + 1
        self.max_durability = self.durability

    def on_click(self):
        if pygame.mouse.get_pressed()[0]:
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
        self.light = Light(8, self.center, (255, 200, 0), 0.3, self.world,
                           self.world.light_g)
        self.on = 0
        self.started = False
        self.set = False
        self.world.score += 1

        self.world.houses += 1

        self.get_colliding()
        if 'flower' in self.colliding:
            self.world.score += 5
            print('yes')

    def handle_light(self, dt):
        self.default_image, self.hover_image, self.pressed_image = self.get_images(
            'house')
        if self.world.sky.dark:
            self.lighting = True
        else:
            self.started = False
            self.lighting = False
            self.set = False
            self.light.image.set_alpha(0)

        if self.lighting:
            if not self.started:
                self.on = random.randint(10, 120)
                self.started = True
            else:
                self.on -= dt
                if self.on < 0:
                    if not self.set:
                        self.default_image, self.hover_image, self.pressed_image = self.get_images(
                            'house_light')
                        self.light.image.set_alpha(self.light.density * 255)
                        self.set = True
        else:
            self.light.image.set_alpha(0)


class Mine(Tile):
    def __init__(self, pos, world, *group):
        super().__init__('mine', pos, world, *group)
        self.lighting = False
        self.light = Light(8, self.center, (255, 200, 0), 0.3, self.world,
                           self.world.light_g)
        self.on = 0
        self.started = False
        self.world.score += 5

        self.world.mines += 1

        self.get_colliding()
        self.around = ['stone' in n for n in self.colliding].count(True)

        self.max_tick = 3600 // self.around
        self.tick = self.max_tick

    def on_update(self, dt):
        self.tick -= dt
        if self.tick <= 0:
            self.tick = self.max_tick
            self.world.stone += 1


class Grass(Tile):
    def __init__(self, name, pos, world, *group):
        super().__init__(name, pos, world, *group)
        self.max_tick = random.randint(GROWTH_MIN, GROWTH_MAX)
        self.tick = self.max_tick

    def grow(self):
        self.name = 'tall_grass'

        tall_grass_count = 0
        trees_count = 0
        flowers_count = 0

        self.get_colliding()
        for other in self.colliding:

            if other == 'tall_grass':
                tall_grass_count += 1
            elif 'tree' in other:
                trees_count += 1
            elif other == 'flower':
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
            elif random.randint(1, 1000) == 1:
                self.name = 'flower'
                print('flower grown')
                break
            elif tall_grass_count > 5:
                self.name = 'tall_grass'
                break

        self.default_image, self.hover_image, self.pressed_image = self.get_images(
            self.name)
        self.image = self.default_image

    def on_click(self):
        if pygame.mouse.get_pressed()[2]:
            if self.house_available:
                if self.check_house_cost():
                    self.buy_house()
                    House(self.pos, self.world, self.groups())
                    self.kill()

            elif self.mine_available:
                if self.check_mine_cost():
                    self.buy_mine()
                    Mine(self.pos, self.world, self.groups())
                    self.kill()

        elif pygame.mouse.get_pressed()[0]:
            self.name = 'grass'

            self.default_image, self.hover_image, self.pressed_image = self.get_images(
                self.name)
            self.image = self.default_image

            self.max_tick = random.randint(GROWTH_MIN, GROWTH_MAX)
            self.tick = self.max_tick

    def on_update(self, dt):
        if self.name not in ('tall_grass', 'flower'):
            self.tick -= 1 * dt
            if self.tick <= 0:
                self.max_tick = random.randint(GROWTH_MIN, GROWTH_MAX)
                self.tick = self.max_tick
                if random.randint(1, 5) == 1:
                    self.grow()
