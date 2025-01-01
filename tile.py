import pygame
import random

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

        self.image = load_image(self.name)

        self.hover_outline = load_image('hover')
        self.pressed_outline = load_image('pressed')
        self.house_image = load_image('build_house')
        self.mine_image = load_image('build_mine')

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

        self.center = self.rect.center

        self.clicked = False
        self.house_available = False
        self.mine_available = False

        self.colliding_checked = False

        self.colliding = []

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

    def draw_house(self):
        self.world.screen.blit(self.house_image, self.rect.topleft)

    def draw_mine(self):
        self.world.screen.blit(self.mine_image, self.rect.topleft)

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

            if not self.colliding_checked:
                self.get_colliding()
                self.check_house_build()
                self.check_mine_build()
                self.colliding_checked = True

            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                self.draw_pressed()

                if not self.clicked:
                    self.on_click()
                    self.clicked = True

            else:
                self.draw_hover()

                if self.house_available:
                    if self.check_house_cost():
                        self.draw_house()
                elif self.mine_available:
                    if self.check_mine_cost():
                        self.draw_mine()

                self.clicked = False
        else:
            self.colliding_checked = False
            self.clicked = False

    def move(self):
        self.rect.topleft = (self.pos[0] + self.world.rect.x,
                             self.pos[1] + self.world.rect.y)
        self.collision_rect.center = self.rect.center

    def check_house_build(self):
        check = [n in ('grass', 'flower') for n in self.colliding]
        if all(check) and self.name == 'grass':
            self.house_available = True
        else:
            self.house_available = False

    def check_mine_build(self):
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

        self.world.score += 1
        self.world.houses += 1


class Mine(Tile):
    def __init__(self, pos, world, *group):
        super().__init__('mine', pos, world, *group)

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
