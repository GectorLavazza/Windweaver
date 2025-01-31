from random import randint, choice

import pygame
from pygame import Rect, mouse, draw, Surface
from pygame.sprite import Sprite

from load_image import load_image
from settings import GROWTH_MIN, GROWTH_MAX, STONE_COST, WOOD_COST


class Tile(Sprite):
    def __init__(self, name, pos, world, *group):
        super().__init__(*group)
        self.world = world

        self.name = name
        self.durability = 0
        self.max_durability = self.durability

        self.image = self.world.images[self.name]

        self.pos = pos

        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] + self.world.rect.x,
                             pos[1] + self.world.rect.y)

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

        self.zone = Rect(*self.rect.topleft,
                         self.rect.width * 3,
                         self.rect.height * 3)
        self.zone.center = self.rect.center

        self.usage_zone = Rect(*self.rect.topleft,
                               self.rect.width * 7,
                               self.rect.height * 7)
        self.usage_zone.center = self.rect.center

    def update(self, dt):
        if self.world.check_moving():
            self.move()
        if self.name not in (
                'house', 'farmland_0', 'farmland_1', 'farmland_2',
                'windmill_1',
                'windmill_2', 'mine'):
            if self.rect.colliderect(self.world.screen_rect):
                self.handle_mouse()
                self.on_update(dt)
        else:
            self.handle_mouse()
            self.on_update(dt)

    def draw_hover(self):
        self.world.screen.blit(self.world.hover_outline, self.rect.topleft)

    def draw_pressed(self):
        self.world.screen.blit(self.world.pressed_outline, self.rect.topleft)

    def draw_build(self):
        image = self.world.build_images[self.world.current_build]
        image.set_alpha(128)
        self.world.screen.blit(image, self.rect.topleft)

    def on_update(self, dt):
        pass

    def on_click(self):
        pass

    def on_kill(self):
        pass

    def handle_mouse(self):
        mouse_pos = mouse.get_pos()

        if self.in_zone():
            if self.rect.collidepoint(mouse_pos):
                if not self.colliding_checked:
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
        self.rect.topleft = (self.pos[0] + self.world.rect.x,
                             self.pos[1] + self.world.rect.y)
        self.collision_rect.center = self.rect.center
        self.area.center = self.rect.center
        self.zone.center = self.rect.center
        self.usage_zone.center = self.rect.center

    def in_zone(self):
        return (any([self.rect.colliderect(p.zone) for p in
                     self.world.pathways_g.sprites() + self.world.buildings_g.sprites()])
                or not self.world.house_placed)

    def check_build(self):
        build = self.world.current_build
        self.available = False

        if self.in_zone():
            if build == 'pathway':
                check_1 = [self.rect.colliderect(p.collision_rect) and
                           (p.rect.centerx == self.rect.centerx or p.rect.centery == self.rect.centery)
                           for p in self.world.pathways_g.sprites()]
                check_2 = [self.rect.colliderect(p.collision_rect) and
                           (p.rect.centerx == self.rect.centerx or p.rect.centery == self.rect.centery)
                           for p in self.world.buildings_g.sprites()]

                if any(check_1) or any(check_2):
                    self.available = True

            elif build == 'house':
                if not self.world.house_placed:
                    self.available = True
                else:
                    check_1 = [self.rect.colliderect(p.collision_rect) and
                               (p.rect.centerx == self.rect.centerx or p.rect.centery == self.rect.centery)
                               for p in self.world.pathways_g.sprites()]

                    if any(check_1):
                        self.available = True

            elif build == 'mine':
                check_1 = [self.rect.colliderect(p.collision_rect) and
                           (p.rect.centerx == self.rect.centerx or p.rect.centery == self.rect.centery)
                           for p in self.world.pathways_g.sprites()]
                check_2 = [self.rect.colliderect(p.collision_rect)
                           for p in self.world.stones_g.sprites()]
                check_3 = [self.rect.colliderect(p.collision_rect) for p in self.world.buildings_g.sprites()]

                if any(check_1) and check_2.count(True) > 1 and not any(check_3) and self.world.houses // 4 > self.world.mines:
                    self.available = True

            elif build == 'windmill':
                check_1 = [self.rect.colliderect(p.collision_rect) and
                           (p.rect.centerx == self.rect.centerx or p.rect.centery == self.rect.centery)
                           for p in self.world.pathways_g.sprites() + self.world.farmland_g.sprites()]
                check_2 = [self.rect.colliderect(p.collision_rect) for p in self.world.buildings_g.sprites()]

                if any(check_1) and not any(check_2) and self.world.houses // 2 > self.world.windmills:
                    self.available = True

            elif build == 'barn':
                check_1 = [self.rect.colliderect(p.collision_rect) and
                           (p.rect.centerx == self.rect.centerx or p.rect.centery == self.rect.centery)
                           for p in self.world.pathways_g.sprites()]

                if any(check_1):
                    self.available = True

    def buy(self):
        build = self.world.current_build
        stone = STONE_COST[build]
        wood = WOOD_COST[build]

        if self.available:
            if self.world.stone - stone >= 0 and self.world.wood - wood >= 0:

                self.world.stone -= stone
                self.world.wood -= wood

                if self.world.house_placed:
                    if build == 'house':
                        House(self.pos, self.world, self.world.buildings_g)
                    elif build == 'mine':
                        Mine(self.pos, self.world, self.world.buildings_g)
                    elif build == 'windmill':
                        Windmill(self.pos, self.world, self.world.buildings_g)
                    elif build == 'pathway':
                        Pathway(self.pos, self.world, self.world.pathways_g)
                    elif build == 'barn':
                        Barn(self.pos, self.world, self.world.buildings_g)
                    self.kill()

                else:
                    if build == 'house':
                        House(self.pos, self.world, self.world.buildings_g)

                        self.kill()


class Grass(Tile):
    def __init__(self, name, pos, world, *group):
        super().__init__(name, pos, world, *group)
        self.max_tick = randint(GROWTH_MIN, GROWTH_MAX)
        self.tick = self.max_tick

    def grow(self):
        if randint(1, 10) == 1:

            if randint(1, 1000) == 1:
                Tree(self.pos, self.world, 0, self.world.trees_g)
                self.kill()
            elif randint(1, 500) == 1:
                self.name = 'flower'
            else:
                self.name = 'tall_grass'

            self.image = load_image(self.name)

    def on_click(self):
        if mouse.get_pressed()[2]:
            if self.available:
                self.buy()

        elif mouse.get_pressed()[0]:
            self.name = 'grass'

            self.image = load_image(self.name)

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
    def __init__(self, pos, world, age, *group):
        super().__init__(f'tree_{age}', pos, world, *group)

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
        Grass('grass', self.pos, self.world, self.world.grass_g)

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
                self.max_tick = randint(GROWTH_MIN, GROWTH_MAX)
                self.tick = self.max_tick
                if randint(1, 10 * (self.age + 1)) == 1:
                    self.grow()


class Stone(Tile):
    def __init__(self, pos, world, amount, *group):
        super().__init__(f'stone_{amount}', pos, world, *group)
        self.amount = amount
        self.durability = self.amount + 1
        self.max_durability = self.durability

    def on_click(self):
        if mouse.get_pressed()[0]:
            self.durability -= 1
            if self.durability <= 0:
                self.on_kill()

    def on_kill(self):
        Grass('grass', self.pos, self.world, self.world.grass_g)
        self.world.stone += self.amount
        self.kill()


class House(Tile):
    def __init__(self, pos, world, *group):
        super().__init__('house', pos, world, *group)
        if not self.world.house_placed:
            self.world.house_placed = True

        self.light = load_image('house_light')
        self.no_light = load_image('house')

        self.max_tick = 600
        self.tick = self.max_tick

        self.zone = Rect(*self.rect.topleft,
                         self.rect.width * 5,
                         self.rect.height * 5)
        self.zone.center = self.rect.center

        self.food = 10
        self.max_food = 10

    def on_update(self, dt):
        if self.world.sky.dark:
            self.image = self.light
        else:
            self.image = self.no_light

        self.tick -= dt
        if self.tick <= 0:
            self.tick = self.max_tick

            v = [p for p in self.world.buildings_g.sprites() if
                         self.rect.colliderect(p.usage_zone) and p.name == 'barn' and p.food > 0]
            print(v)
            if v:
                barn = choice(v)
                barn.food -= 1


    def draw_hover(self):
        self.world.screen.blit(self.world.hover_outline, self.rect.topleft)
        self.draw_stats()

    def draw_pressed(self):
        self.world.screen.blit(self.world.pressed_outline, self.rect.topleft)
        # self.draw_stats()

    def draw_stats(self):
        draw.rect(self.world.screen, '#46474c', Rect(self.rect.x, self.rect.y - 2, self.rect.w, 1))
        draw.rect(self.world.screen, '#e0dca4',
                  Rect(self.rect.x, self.rect.y - 2, self.rect.w / self.max_food * self.food, 1))


class Mine(Tile):
    def __init__(self, pos, world, *group):
        super().__init__('mine', pos, world, *group)
        self.around = ['stone' in n.name for n in self.colliding].count(True)

        self.max_tick = 1800
        self.tick = self.max_tick

        self.zone = Rect(*self.rect.topleft,
                         self.rect.width * 5,
                         self.rect.height * 5)
        self.zone.center = self.rect.center

    def on_update(self, dt):
        self.tick -= dt
        if self.tick <= 0:
            self.tick = self.max_tick
            self.world.stone += 1


class Windmill(Tile):
    def __init__(self, pos, world, *group):
        super().__init__('windmill_1', pos, world, *group)

        self.max_tick = 60
        self.tick = self.max_tick

        self.frame = 1
        self.max_animation_tick = 30
        self.animation_tick = self.max_animation_tick

        self.frames = {
            1: load_image('windmill_1'),
            2: load_image('windmill_2')
        }

        self.zone = Rect(*self.rect.topleft,
                         self.rect.width * 5,
                         self.rect.height * 5)
        self.zone.center = self.rect.center

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
            tiles = [p for p in self.world.grass_g.sprites() + self.world.pathways_g.sprites() if
                     self.rect.colliderect(p.collision_rect) and p.name in ('grass', 'pathway') and p.in_zone()]
            if tiles:
                tile = choice(tiles)
                Farmland(tile.pos, tile.world, self.world.farmland_g)
                tile.kill()


class Farmland(Tile):
    def __init__(self, pos, world, *group):
        self.age = 0

        super().__init__(f'farmland_{self.age}', pos, world, *group)

        self.max_tick = randint(300, 600)
        self.tick = self.max_tick

        self.max_spread_tick = 600
        self.spread_tick = self.max_spread_tick

    def grow(self):
        if randint(1, 2) == 1:
            self.age += 1
            self.name = f'farmland_{self.age}'
            self.image = load_image(self.name)

    def on_update(self, dt):
        if self.age < 2:
            self.tick -= 1 * dt
            if self.tick <= 0:
                self.max_tick = randint(600, 1200)
                self.tick = self.max_tick
                self.grow()

    def on_click(self):
        if self.age == 2:
            self.max_tick = randint(300, 600)
            self.tick = self.max_tick

            self.age = 0
            self.name = f'farmland_{self.age}'
            self.image = load_image(self.name)

            self.world.food += 2


class Pathway(Tile):
    def __init__(self, pos, world, *group):
        super().__init__('pathway', pos, world, *group)


class Barn(Tile):
    def __init__(self, pos, world, *group):
        super().__init__('barn', pos, world, *group)

        if not self.world.house_placed:
            self.world.house_placed = True

        self.zone = Rect(*self.rect.topleft,
                         self.rect.width * 5,
                         self.rect.height * 5)
        self.zone.center = self.rect.center

        self.food = 50
        self.capacity = 50

    def draw_hover(self):
        self.world.screen.blit(self.world.hover_outline, self.rect.topleft)
        self.draw_stats()

    def draw_pressed(self):
        self.world.screen.blit(self.world.pressed_outline, self.rect.topleft)
        self.draw_stats()

    def draw_stats(self):
        surface = Surface(self.usage_zone.size, pygame.SRCALPHA)
        surface.set_alpha(40)
        surface.fill('blue')
        self.world.screen.blit(surface, self.usage_zone.topleft)
        draw.rect(self.world.screen, 'blue', self.usage_zone, 1)
        draw.rect(self.world.screen, '#46474c', Rect(self.rect.x, self.rect.y - 2, self.rect.w, 1))
        draw.rect(self.world.screen, '#e0dca4',
                  Rect(self.rect.x, self.rect.y - 2, self.rect.w / self.capacity * self.food, 1))
