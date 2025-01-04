from random import randint, choice

from pygame import Rect, mouse
from pygame.sprite import Sprite

from settings import GROWTH_MIN, GROWTH_MAX, STONE_COST, WOOD_COST


class Tile(Sprite):
    def __init__(self, name, pos, chunk, *group):
        super().__init__(*group)
        self.chunk = chunk
        self.images = self.chunk.world.engine.images

        self.name = name
        self.durability = 0
        self.max_durability = self.durability

        self.image = self.chunk.images[self.name]

        self.pos = pos

        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] + self.chunk.rect.x,
                             pos[1] + self.chunk.rect.y)

        self.center = self.pos[0] + self.rect.w // 2, self.pos[
            1] + self.rect.h // 2

        self.collision_rect = Rect(*self.rect.topleft,
                                   self.rect.width * 2,
                                   self.rect.height * 2)
        self.collision_rect.center = self.rect.center

        self.area = Rect(*self.rect.topleft,
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
        if self.chunk.check_mouse_edges():
            self.move()
        if self.name not in (
                'house', 'farmland_0', 'farmland_1', 'farmland_2',
                'windmill_1',
                'windmill_2', 'mine'):
            if self.rect.colliderect(self.chunk.screen_rect):
                self.handle_mouse()
                self.on_update(dt)
        else:
            self.handle_mouse()
            self.on_update(dt)

    def draw_hover(self):
        self.chunk.screen.blit(self.chunk.hover_outline, self.rect.topleft)

    def draw_pressed(self):
        self.chunk.screen.blit(self.chunk.pressed_outline, self.rect.topleft)

    def draw_build(self):
        image = self.chunk.build_images[self.chunk.current_build]
        self.chunk.screen.blit(image, self.rect.topleft)

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
        mouse_pos = mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if not self.colliding_checked:
                self.get_colliding()
                self.get_in_area()
                self.colliding_checked = True

                if self.name == 'grass':
                    self.check_build()

            if mouse.get_pressed()[0] or mouse.get_pressed()[2]:
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
        self.rect.topleft = (self.pos[0] + self.chunk.rect.x,
                             self.pos[1] + self.chunk.rect.y)
        self.collision_rect.center = self.rect.center
        self.area.center = self.rect.center

    def check_build(self):
        build = self.chunk.current_build
        if build == 'house':
            names = [n.name for n in self.colliding]
            check = [n in (
                'grass', 'flower', 'pathway', 'farmland_0', 'farmland_1',
                'farmland_2') for n in names]
            if not self.chunk.house_placed and all(
                    check) or self.chunk.house_placed and all(
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
                if self.chunk.houses // 5 >= (self.chunk.mines + 1):
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
                if self.chunk.houses // 2 >= (self.chunk.windmills + 1):
                    self.available = True
            else:
                self.available = False

    def buy(self):
        build = self.chunk.current_build
        stone = STONE_COST[build]
        wood = WOOD_COST[build]

        if self.chunk.stone - stone >= 0 and self.chunk.wood - wood >= 0:

            self.chunk.stone -= stone
            self.chunk.wood -= wood

            if build == 'house':
                House(self.pos, self.chunk, self.groups())
            elif build == 'mine':
                Mine(self.pos, self.chunk, self.groups())
            elif build == 'windmill':
                Windmill(self.pos, self.chunk, self.groups())

            self.kill()


class Grass(Tile):
    def __init__(self, name, pos, chunk, *group):
        super().__init__(name, pos, chunk, *group)
        self.max_tick = randint(GROWTH_MIN, GROWTH_MAX)
        self.tick = self.max_tick

    def grow(self):
        if randint(1, 10) == 1:

            if randint(1, 1000) == 1:
                Tree(self.pos, self.chunk, 0, self.groups())
                self.kill()
            elif randint(1, 500) == 1:
                self.name = 'flower'
            else:
                self.name = 'tall_grass'

            self.image = self.images[self.name]

    def on_click(self):
        if mouse.get_pressed()[2]:
            if self.available:
                self.buy()

        elif mouse.get_pressed()[0]:
            self.name = 'grass'

            self.image = self.images[self.name]

            self.max_tick = randint(GROWTH_MIN, GROWTH_MAX)
            self.tick = self.max_tick

    def on_update(self, dt):
        if self.name not in ('tall_grass', 'flower'):
            self.tick -= 1 * dt
            if self.tick <= 0:
                self.max_tick = randint(GROWTH_MIN, GROWTH_MAX)
                self.tick = self.max_tick
                self.grow()


class Tree(Tile):
    def __init__(self, pos, chunk, age, *group):
        super().__init__(f'tree_{age}', pos, chunk, *group)

        self.max_tick = randint(GROWTH_MIN, GROWTH_MAX)
        self.tick = self.max_tick

        self.durability = age + 2
        self.max_durability = self.durability
        self.age = age

    def on_click(self):
        if mouse.get_pressed()[0]:
            self.durability -= 1
            if self.durability <= 0:
                self.on_kill()

    def on_kill(self):
        Grass('grass', self.pos, self.chunk, self.groups())

        self.chunk.world.wood += self.age + 1
        self.kill()

    def grow(self):
        self.age += 1
        self.durability = self.age + 2
        self.max_durability = self.durability

        self.name = f'tree_{self.age}'

        self.image = self.images[self.name]

    def on_update(self, dt):
        if self.age < 2:
            self.tick -= 1 * dt
            if self.tick <= 0:
                self.max_tick = randint(GROWTH_MIN, GROWTH_MAX)
                self.tick = self.max_tick
                if randint(1, 10 * (self.age + 1)) == 1:
                    self.grow()


class Stone(Tile):
    def __init__(self, pos, chunk, amount, *group):
        super().__init__(f'stone_{amount}', pos, chunk, *group)
        self.amount = amount
        self.durability = self.amount + 1
        self.max_durability = self.durability

    def on_click(self):
        if mouse.get_pressed()[0]:
            self.durability -= 1
            if self.durability <= 0:
                self.on_kill()

    def on_kill(self):
        Grass('grass', self.pos, self.chunk, self.groups())
        self.chunk.world.stone += self.amount
        self.kill()


class House(Tile):
    def __init__(self, pos, chunk, *group):
        super().__init__('house', pos, chunk, *group)
        self.chunk.world.houses += 1

        if not self.chunk.house_placed:
            self.chunk.house_placed = True

        self.light = self.images['house_light']
        self.no_light = self.images['house']

        self.max_spread_tick = 120
        self.spread_tick = self.max_spread_tick

        self.spread_count = 1

        self.pathway = self.make_pathway()

        self.max_tick = 3600
        self.tick = self.max_tick

    def on_update(self, dt):
        if self.chunk.world.sky.dark:
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
            self.chunk.world.food -= 1

    def make_pathway(self):
        sides = self.get_sides()
        tiles = list(filter(lambda
                                n: n.name == 'grass' and n.rect.topleft != self.rect.topleft,
                            sides))
        if tiles:
            tile = choice(tiles)
            pathway = Pathway(tile.pos, tile.chunk, self.groups())
            tile.kill()

            return pathway

        return 0


class Mine(Tile):
    def __init__(self, pos, chunk, *group):
        super().__init__('mine', pos, chunk, *group)
        self.chunk.world.mines += 1

        self.around = ['stone' in n.name for n in self.colliding].count(True)

        self.max_tick = 3600
        self.tick = self.max_tick

    def on_update(self, dt):
        self.tick -= dt
        if self.tick <= 0:
            self.tick = self.max_tick
            self.chunk.world.stone += 1


class Windmill(Tile):
    def __init__(self, pos, chunk, *group):
        super().__init__('windmill_1', pos, chunk, *group)

        self.max_tick = 120
        self.tick = self.max_tick

        self.chunk.world.windmills += 1

        self.frame = 1
        self.max_animation_tick = 30
        self.animation_tick = self.max_animation_tick

        self.frames = {
            1: self.images['windmill_1'],
            2: self.images['windmill_2']
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
        if randint(1, 2) == 1:
            self.get_colliding()
            tiles = list(filter(lambda n: n.name == 'grass', self.colliding))
            if tiles:
                tile = choice(tiles)
                Farmland(tile.pos, tile.chunk, self.groups())
                tile.kill()


class Farmland(Tile):
    def __init__(self, pos, chunk, *group):
        self.age = 0

        super().__init__(f'farmland_{self.age}', pos, chunk, *group)

        self.max_tick = randint(1800, 3600)
        self.tick = self.max_tick

        self.max_spread_tick = 600
        self.spread_tick = self.max_spread_tick

    def grow(self):
        if randint(1, 5) == 1:
            self.age += 1
            self.name = f'farmland_{self.age}'
            self.image = self.images[self.name]

    def on_update(self, dt):
        if self.age < 2:
            self.tick -= 1 * dt
            if self.tick <= 0:
                self.max_tick = randint(1800, 3600)
                self.tick = self.max_tick
                self.grow()
        else:
            self.spread_tick -= dt
            if self.spread_tick <= 0:
                self.spread_tick = self.max_spread_tick
                self.spread()

    def spread(self):
        if randint(1, 2) == 1:
            self.get_colliding()
            tiles = list(filter(lambda n: n.name == 'grass', self.colliding))
            if tiles:
                tile = choice(tiles)
                Farmland(tile.pos, tile.chunk, self.groups())
                tile.kill()

    def on_click(self):
        if self.age == 2:
            self.max_tick = randint(1800, 3600)
            self.tick = self.max_tick

            self.age = 0
            self.name = f'farmland_{self.age}'
            self.image = self.images[self.name]

            self.chunk.world.food += 2


class Pathway(Tile):
    def __init__(self, pos, chunk, *group):
        super().__init__('pathway', pos, chunk, *group)

        self.max_spread_tick = 120
        self.spread_tick = self.max_spread_tick

        self.spreaded = False

    def spread(self):
        sides = self.get_sides()
        tiles = list(filter(lambda n: n.name == 'grass', sides))
        check = [n.name for n in self.colliding]
        if tiles and check.count('pathway') < 2:
            tile = choice(tiles)
            Pathway(tile.pos, tile.chunk, self.groups())
            tile.kill()
            self.spreaded = True
