import random

import pygame

from load_image import load_image
from settings import GROWTH_MIN, GROWTH_MAX, STONE_COST, WOOD_COST
from sprite import Sprite


class Tile(Sprite):
    def __init__(self, name, pos, world, *group):
        super().__init__(*group)
        self.world = world

        self.name = name
        self.durability = 0
        self.max_durability = self.durability

        self.image = load_image(self.name)

        self.hover_outline = load_image('hover')
        self.pressed_outline = load_image('pressed')

        self.build_images = {
            'house': load_image('build_house'),
            'mine': load_image('build_mine'),
            'windmill': load_image('windmill_build')
        }

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

        self.area = pygame.rect.Rect(*self.rect.topleft,
                                     self.rect.width * 7,
                                     self.rect.height * 7)
        self.area.center = self.rect.center

        self.center = self.rect.center

        self.clicked = False
        self.available = False

        self.colliding_checked = False

        self.colliding = []
        self.in_area = []

        self.image_set = False

    def update(self, dt):
        if self.world.check_mouse_edges():
            self.move()

        self.handle_mouse()
        self.on_update(dt)

    def draw_hover(self):
        self.world.screen.blit(self.hover_outline, self.rect.topleft)

    def draw_pressed(self):
        self.world.screen.blit(self.pressed_outline, self.rect.topleft)

    def draw_build(self):
        image = self.build_images[self.world.current_build]
        self.world.screen.blit(image, self.rect.topleft)

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

    def get_in_area(self):
        self.in_area.clear()
        for other in self.groups()[0]:
            if self.area.colliderect(other.rect):
                if other != self:
                    self.in_area.append(other)

    def get_sides(self):
        sides = []

        self.get_colliding()
        for other in self.colliding:
            if other.rect.x == self.rect.x or other.rect.y == self.rect.y:
                sides.append(other)

        return sides

    def handle_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if not self.colliding_checked:
                self.get_colliding()
                self.get_in_area()
                self.colliding_checked = True

                if self.name == 'grass':
                    self.check_build()

            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                self.draw_pressed()

                if not self.clicked:
                    self.on_click()
                    self.clicked = True

            else:
                self.draw_hover()

                if self.available:
                    self.draw_build()

                self.clicked = False
        else:
            self.colliding_checked = False
            self.clicked = False

    def move(self):
        self.rect.topleft = (self.pos[0] + self.world.rect.x,
                             self.pos[1] + self.world.rect.y)
        self.collision_rect.center = self.rect.center
        self.area.center = self.rect.center

    def check_build(self):
        build = self.world.current_build
        if build == 'house':
            names = [n.name for n in self.colliding]
            check = [n in ('grass', 'flower', 'pathway', 'farmland_0', 'farmland_1', 'farmland_2') for n in names]
            if not self.world.house_placed and all(
                    check) or self.world.house_placed and all(
                check) and names.count('pathway') > 0:
                self.available = True
            else:
                self.available = False

        elif build == 'mine':
            check = ['stone' in n.name for n in self.colliding]
            check2 = ['tree' not in n.name and 'mine' not in n.name for n in
                      self.colliding]
            if check.count(True) > 2 and all(check2) and self.colliding.count(
                    'tall_grass') == 0 and self.name == 'grass':
                if self.world.houses // 2 >= (self.world.mines + 1):
                    self.available = True
            else:
                self.available = False

        elif build == 'windmill':
            check = [n.name in (
                'grass', 'pathway', 'farmland_0', 'farmland_1', 'farmland_2')
                     for n
                     in self.colliding]
            in_area = [n.name for n in self.in_area]
            if all(check) and self.name == 'grass' and in_area.count(
                    'house') + in_area.count('windmill_1') + in_area.count(
                'windmill_2') + in_area.count(
                'farmland_0') + in_area.count(
                'farmland_1') + in_area.count('farmland_2') > 0:
                self.available = True
            else:
                self.available = False

    def buy(self):
        build = self.world.current_build
        stone = STONE_COST[build]
        wood = WOOD_COST[build]

        if self.world.stone - stone >= 0 and self.world.wood - wood >= 0:

            self.world.stone -= stone
            self.world.wood -= wood

            if build == 'house':
                House(self.pos, self.world, self.groups())
            elif build == 'mine':
                Mine(self.pos, self.world, self.groups())
            elif build == 'windmill':
                Windmill(self.pos, self.world, self.groups())

            self.kill()


class Grass(Tile):
    def __init__(self, name, pos, world, *group):
        super().__init__(name, pos, world, *group)
        self.max_tick = random.randint(GROWTH_MIN, GROWTH_MAX)
        self.tick = self.max_tick

    def grow(self):
        if random.randint(1, 10) == 1:

            if random.randint(1, 1000) == 1:
                Tree(self.pos, self.world, 0, self.groups())
                self.kill()
            elif random.randint(1, 500) == 1:
                self.name = 'flower'
            else:
                self.name = 'tall_grass'

            self.image = load_image(self.name)

    def on_click(self):
        if pygame.mouse.get_pressed()[2]:
            if self.available:
                self.buy()

        elif pygame.mouse.get_pressed()[0]:
            self.name = 'grass'

            self.image = load_image(self.name)

            self.max_tick = random.randint(GROWTH_MIN, GROWTH_MAX)
            self.tick = self.max_tick

    def on_update(self, dt):
        if self.name not in ('tall_grass', 'flower'):
            self.tick -= 1 * dt
            if self.tick <= 0:
                self.max_tick = random.randint(GROWTH_MIN, GROWTH_MAX)
                self.tick = self.max_tick
                self.grow()


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
        self.age += 1
        self.durability = self.age + 2
        self.max_durability = self.durability

        self.name = f'tree_{self.age}'

        self.image = load_image(self.name)

    def on_update(self, dt):
        if self.age < 2:
            self.tick -= 1 * dt
            if self.tick <= 0:
                self.max_tick = random.randint(GROWTH_MIN, GROWTH_MAX)
                self.tick = self.max_tick
                if random.randint(1, 10 * (self.age + 1)) == 1:
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
        self.world.houses += 1

        if not self.world.house_placed:
            self.world.house_placed = True

        self.light = load_image('house_light')
        self.no_light = load_image('house')

        self.max_spread_tick = 120
        self.spread_tick = self.max_spread_tick

        self.spread_count = 1

        self.pathway = self.make_pathway()

        self.max_tick = 3600
        self.tick = self.max_tick

    def on_update(self, dt):
        if self.world.sky.dark:
            self.image = self.light
        else:
            self.image = self.no_light

        if self.pathway:
            if self.spread_count < 3:
                self.spread_tick -= dt
                if self.spread_tick <= 0:
                    self.spread_count += 1
                    self.spread_tick = self.max_spread_tick
                    self.pathway.spread()

        self.tick -= dt
        if self.tick <= 0:
            self.tick = self.max_tick
            self.world.food -= 1

    def make_pathway(self):
        sides = self.get_sides()
        tiles = list(filter(lambda
                                n: n.name == 'grass' and n.rect.topleft != self.rect.topleft,
                            sides))
        if tiles:
            tile = random.choice(tiles)
            pathway = Pathway(tile.pos, tile.world, self.groups())
            tile.kill()

            return pathway

        return 0


class Mine(Tile):
    def __init__(self, pos, world, *group):
        super().__init__('mine', pos, world, *group)
        self.world.mines += 1

        self.around = ['stone' in n.name for n in self.colliding].count(True)

        self.max_tick = 3600
        self.tick = self.max_tick

    def on_update(self, dt):
        self.tick -= dt
        if self.tick <= 0:
            self.tick = self.max_tick
            self.world.stone += 1


class Windmill(Tile):
    def __init__(self, pos, world, *group):
        super().__init__('windmill_1', pos, world, *group)

        self.max_tick = 120
        self.tick = self.max_tick

        self.frame = 1
        self.max_animation_tick = 30
        self.animation_tick = self.max_animation_tick

        self.frames = {
            1: load_image('windmill_1'),
            2: load_image('windmill_2')
        }

    def on_update(self, dt):
        self.tick -= dt
        if self.tick <= 0:
            self.tick = self.max_tick
            self.spread()

        self.animation_tick -= dt
        if self.animation_tick <= 0:
            self.animation_tick = self.max_animation_tick
            self.change_frame()

    def change_frame(self):
        self.frame = 2 if self.frame == 1 else 1
        self.name = f'windmill_{self.frame}'
        self.image = self.frames[self.frame]

    def spread(self):
        if random.randint(1, 2) == 1:
            self.get_colliding()
            tiles = list(filter(lambda n: n.name == 'grass', self.colliding))
            if tiles:
                tile = random.choice(tiles)
                Farmland(tile.pos, tile.world, self.groups())
                tile.kill()


class Farmland(Tile):
    def __init__(self, pos, world, *group):
        self.age = 0

        super().__init__(f'farmland_{self.age}', pos, world, *group)

        self.max_tick = random.randint(1800, 3600)
        self.tick = self.max_tick

        self.max_spread_tick = 600
        self.spread_tick = self.max_spread_tick

    def grow(self):
        if random.randint(1, 5) == 1:
            self.age += 1
            self.name = f'farmland_{self.age}'
            self.image = load_image(self.name)

    def on_update(self, dt):
        if self.age < 2:
            self.tick -= 1 * dt
            if self.tick <= 0:
                self.max_tick = random.randint(1800, 3600)
                self.tick = self.max_tick
                self.grow()
        else:
            self.spread_tick -= dt
            if self.spread_tick <= 0:
                self.spread_tick = self.max_spread_tick
                self.spread()

    def spread(self):
        if random.randint(1, 2) == 1:
            self.get_colliding()
            tiles = list(filter(lambda n: n.name == 'grass', self.colliding))
            if tiles:
                tile = random.choice(tiles)
                Farmland(tile.pos, tile.world, self.groups())
                tile.kill()

    def on_click(self):
        if self.age == 2:
            self.max_tick = random.randint(1800, 3600)
            self.tick = self.max_tick

            self.age = 0
            self.name = f'farmland_{self.age}'
            self.image = load_image(self.name)

            self.world.food += 2


class Pathway(Tile):
    def __init__(self, pos, world, *group):
        super().__init__('pathway', pos, world, *group)

        self.max_spread_tick = 120
        self.spread_tick = self.max_spread_tick

        self.spreaded = False

    def spread(self):
        sides = self.get_sides()
        tiles = list(filter(lambda n: n.name == 'grass', sides))
        check = [n.name for n in self.colliding]
        if tiles and check.count('pathway') < 2:
            tile = random.choice(tiles)
            Pathway(tile.pos, tile.world, self.groups())
            tile.kill()
            self.spreaded = True
