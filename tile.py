from random import randint, choice

import pygame
from pygame import Rect, mouse, draw, Surface
from pygame.sprite import Sprite

from light import Light
from settings import *
from particles import create_particles


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
                                   self.rect.width * 1.5,
                                   self.rect.height * 1.5)
        self.collision_rect.center = self.rect.center

        self.area = Rect(*self.rect.topleft,
                         self.rect.width * 7,
                         self.rect.height * 7)
        self.area.center = self.rect.center

        self.center = self.rect.center

        self.clicked = False
        self.available = False

        self.image_set = False

        self.zone = Rect(*self.rect.topleft,
                         self.rect.width * 3,
                         self.rect.height * 3)
        self.zone.center = self.rect.center

        self.usage_zone = Rect(*self.rect.topleft,
                               self.rect.width * 7,
                               self.rect.height * 7)
        self.usage_zone.center = self.rect.center

        self.stats_offset = 0
        self.alpha = 0
        self.stats_alpha = 0
        self.usage_zone_alpha = 0
        self.flash_d = 1
        self.building_alpha = 80

    def update(self, dt):
        if self.world.check_moving():
            self.move()

        self.handle_mouse(dt)
        self.on_update(dt)

    def draw_hover(self):
        self.world.screen.blit(self.world.hover_outline, self.rect.topleft)

    def draw_pressed(self):
        self.world.screen.blit(self.world.pressed_outline, self.rect.topleft)

    def draw_stats(self, dt):
        pass

    def draw_build(self, dt):
        image = self.world.build_images[self.world.current_build]
        self.building_alpha += self.flash_d * dt * 2
        if self.building_alpha > 160:
            self.flash_d = -1
        if self.building_alpha < 80:
            self.flash_d = 1
        image.set_alpha(self.building_alpha)
        self.world.screen.blit(image, self.rect.topleft)

    def on_update(self, dt):
        pass

    def on_click(self):
        pass

    def on_kill(self):
        pass

    def handle_mouse(self, dt):
        mouse_pos = mouse.get_pos()
        if self.stats_alpha > 0:
            self.draw_stats(dt)

        if self.usage_zone_alpha > 0:
            self.draw_usage_zone()

        if self.rect.collidepoint(mouse_pos):
            if self.available:
                self.draw_build(dt)

            self.stats_offset = min(4 * SCALE, self.stats_offset + dt * STATS_OFFSET_SPEED)
            self.stats_alpha = min(int(self.stats_alpha + dt * STATS_ALPHA_SPEED), 255) \
                if self.name not in ('barn', 'mine') and 'windmill' not in self.name else 255
            self.usage_zone_alpha = min(int(self.usage_zone_alpha + dt * STATS_ALPHA_SPEED), 255)
            if self.name == 'grass':
                self.check_build()

            if mouse.get_pressed()[0] or mouse.get_pressed()[2]:
                if not self.clicked:
                    if not self.world.removing:
                        self.on_click()
                    self.clicked = True
                self.alpha = min(int(self.alpha + dt * OUTLINE_ALPHA_SPEED), 100)
                self.world.pressed_outline.set_alpha(self.alpha)
                self.draw_pressed()

                if self.world.removing:
                    if self.world.buildings_g in self.groups() or self.world.pathways_g in self.groups():
                            if self.world.houses > 1 or 'house' not in self.name:
                                if self.in_zone():
                                    self.on_kill()

            else:
                self.alpha = max(int(self.alpha - dt * OUTLINE_ALPHA_SPEED), min(int(self.alpha + dt * OUTLINE_ALPHA_SPEED), 60))

                self.world.hover_outline.set_alpha(self.alpha)

                self.draw_hover()

                self.clicked = False
        else:
            self.clicked = False
            self.stats_offset = max(0, self.stats_offset - dt * STATS_OFFSET_SPEED)
            self.stats_alpha = max(int(self.stats_alpha - dt * STATS_ALPHA_SPEED), 0) \
                if self.name not in ('barn', 'mine') and 'windmill' not in self.name else 255
            self.usage_zone_alpha = max(int(self.usage_zone_alpha - dt * STATS_ALPHA_SPEED), 0)
            self.alpha = 0

    def move(self):
        self.rect.topleft = (self.pos[0] + self.world.rect.x,
                             self.pos[1] + self.world.rect.y)
        self.collision_rect.center = self.rect.center
        self.area.center = self.rect.center
        self.zone.center = self.rect.center
        self.usage_zone.center = self.rect.center

    def in_zone(self):
        return (self.rect.collidelist(self.world.zone) != -1
                or (not self.world.house_placed and self.name == 'grass'))

    def check_build(self):
        build = self.world.current_build
        self.available = False

        if build == 'pathway':
            check_1 = [self.rect.colliderect(p.collision_rect) and
                       (p.rect.centerx == self.rect.centerx or p.rect.centery == self.rect.centery)
                       for p in self.world.pathways_g.sprites()]
            check_2 = [self.rect.colliderect(p.collision_rect) and
                       (p.rect.centerx == self.rect.centerx or p.rect.centery == self.rect.centery)
                       for p in self.world.buildings_g.sprites()]

            if (any(check_1) or any(check_2)) and self.world.houses > self.world.pathways // 5:
                self.available = True

        elif build == 'house':
            if not self.world.house_placed:
                self.available = True
            else:
                check_1 = [self.rect.colliderect(p.collision_rect) and
                           (p.rect.centerx == self.rect.centerx or p.rect.centery == self.rect.centery)
                           for p in self.world.pathways_g.sprites()]
                check_2 = [self.rect.colliderect(p.collision_rect) and (p.name == 'mine' or 'windmill' in p.name) for p in self.world.buildings_g.sprites()]

                if any(check_1) and not any(check_2):
                    self.available = True

        elif build == 'mine':
            check_1 = [self.rect.colliderect(p.collision_rect) and
                       (p.rect.centerx == self.rect.centerx or p.rect.centery == self.rect.centery)
                       for p in self.world.pathways_g.sprites()]
            check_2 = [self.rect.colliderect(p.collision_rect)
                       for p in self.world.stones_g.sprites()]
            check_3 = [self.rect.colliderect(p.collision_rect) for p in self.world.buildings_g.sprites()]

            #  and check_2.count(True) > 1
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
            check_2 = [self.rect.colliderect(p.collision_rect) and (p.name == 'mine' or 'windmill' in p.name) for p in
                       self.world.buildings_g.sprites()]

            if any(check_1) and not any(check_2):
                self.available = True

        elif build == 'storage':
            check_1 = [self.rect.colliderect(p.collision_rect) and
                       (p.rect.centerx == self.rect.centerx or p.rect.centery == self.rect.centery)
                       for p in self.world.pathways_g.sprites()]
            check_2 = [self.rect.colliderect(p.collision_rect) and (p.name == 'mine' or 'windmill' in p.name) for p in
                       self.world.buildings_g.sprites()]

            if any(check_1) and not any(check_2):
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
                    elif build == 'storage':
                        Storage(self.pos, self.world, self.world.buildings_g)
                    self.kill()

                else:
                    if build == 'house':
                        House(self.pos, self.world, self.world.buildings_g)

                        self.kill()

    def draw_usage_zone(self):
        pass


class Grass(Tile):
    def __init__(self, name, pos, world, *group):
        super().__init__(name, pos, world, *group)
        self.max_tick = randint(GROWTH_MIN, GROWTH_MAX)
        self.tick = self.max_tick

    def on_click(self):
        if mouse.get_pressed()[2]:
            if self.available:
                if self.in_zone():
                    self.buy()

        elif mouse.get_pressed()[0]:
            if self.in_zone():
                if self.name == 'tall_grass':
                    create_particles(GREEN, self.rect.center, 5, 15, self.world.particles_g)

                self.name = 'grass'

                self.image = self.world.images[self.name]

                self.max_tick = randint(GROWTH_MIN, GROWTH_MAX)
                self.tick = self.max_tick


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
            if self.in_zone():
                self.durability -= 1
                create_particles(GREEN, self.rect.center, 5 * (self.age + 1), 15, self.world.particles_g)
                if self.durability <= 0:
                    self.on_kill()

    def on_kill(self):
        if self.world.max_wood > self.world.wood:
            amount = self.age + 1
            d = self.world.max_wood - self.world.wood
            if d > amount:
                d = amount
            self.world.wood += d

        Grass('grass', self.pos, self.world, self.world.grass_g)
        self.kill()

    def grow(self):
        self.age += 1
        self.durability = self.age + 2
        self.max_durability = self.durability

        self.name = f'tree_{self.age}'

        self.image = self.world.images[self.name]

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
            if self.in_zone():
                self.durability -= 1
                create_particles(GREY, self.rect.center, self.amount * 2, 15, self.world.particles_g)
                if self.durability <= 0:
                    self.on_kill()

    def on_kill(self):
        if self.world.max_stone > self.world.stone:
            d = self.world.max_stone - self.world.stone
            if d > self.amount:
                d = self.amount
            self.world.stone += d
        Grass('grass', self.pos, self.world, self.world.grass_g)
        self.kill()


class House(Tile):
    def __init__(self, pos, world, *group):
        super().__init__('house', pos, world, *group)
        if not self.world.house_placed:
            self.world.house_placed = True

        # self.light = Light(self.world.screen, 6, (30, 30, 10), 1)
        # self.light.rect.center = self.rect.center

        self.max_tick = 1200
        self.tick = self.max_tick

        self.zone = Rect(*self.rect.topleft,
                         self.rect.width * 5,
                         self.rect.height * 5)
        self.zone.center = self.rect.center

        self.food = 5
        self.capacity = 5

        self.world.update_zone()
        self.food_w = (self.rect.w * 2) / self.capacity * self.food

        # self.l = Light(10, self.rect.center, (255, 0, 0), 1, self.world, self.world.light_g)

    def on_update(self, dt):
        # if self.world.sky.dark:
        #     self.light.rect.center = self.rect.center
        #     # self.light.update()

        self.tick -= dt
        if self.tick <= 0:
            self.tick = self.max_tick

            self.food -= 1
            d = self.capacity - self.food
            v = [p for p in self.world.buildings_g.sprites() if
                         self.rect.colliderect(p.usage_zone) and p.name == 'barn' and p.food - d >= 0]
            if v:
                barn = choice(v)
                barn.food -= d
                self.food += d

        if self.food < 1:
            self.kill()
            Grass('grass', self.pos, self.world, self.world.grass_g)
            create_particles(BLACK, self.rect.center, 10, 15, self.world.particles_g)
            self.world.update_zone()

    def draw_stats(self, dt):
        b = Rect(self.rect.x - self.rect.w / 2 - SCALE / 2, self.rect.y - 4 * SCALE + SCALE - self.stats_offset, self.rect.w * 2,
                       2 * SCALE)
        sb = Surface(b.size, pygame.SRCALPHA)
        sb.fill((70, 71, 76, self.stats_alpha))
        self.world.screen.blit(sb, b.topleft)

        self.food_w = max(self.food_w - dt * STATS_BAR_SPEED,
                          min(self.food_w + dt * STATS_BAR_SPEED, (self.rect.w * 2) / self.capacity * self.food))
        f = Rect(self.rect.x - self.rect.w / 2 + SCALE / 2, self.rect.y - 4 * SCALE - self.stats_offset,
                       self.food_w, 2 * SCALE)
        sf = Surface(f.size, pygame.SRCALPHA)
        sf.fill((224, 220, 164, self.stats_alpha))
        self.world.screen.blit(sf, f.topleft)

    def on_kill(self):
        check = [self.rect.colliderect(p.collision_rect) and
         (p.rect.centerx == self.rect.centerx or p.rect.centery == self.rect.centery)
         for p in self.world.pathways_g.sprites()]

        if check.count(True) < 2:
            Grass('grass', self.pos, self.world, self.world.grass_g)

            w, s = randint(1, WOOD_COST['house'] // 2), randint(1, STONE_COST['house'] // 2)

            wd = self.world.max_wood - self.world.wood
            if wd > w:
                wd = w
            self.world.wood += wd

            sd = self.world.max_stone - self.world.stone
            if sd > s:
                sd = s
            self.world.stone += sd
            create_particles(BLACK, self.rect.center, 10, 15, self.world.particles_g)
            self.kill()
            self.world.update_zone()


class Mine(Tile):
    def __init__(self, pos, world, *group):
        super().__init__('mine', pos, world, *group)

        self.max_tick = 300
        self.tick = self.max_tick

        self.zone = Rect(*self.rect.topleft,
                         self.rect.width * 5,
                         self.rect.height * 5)
        self.zone.center = self.rect.center

        self.stone = 0
        self.capacity = 10
        self.max_capacity = 10

        self.collected = 0

        self.world.update_zone()
        self.stone_w = (self.rect.w * 2) / self.capacity * self.stone

    def on_update(self, dt):
        self.draw_stats(dt)
        self.capacity = self.max_capacity - self.collected // 10
        self.capacity = max(1, self.capacity)

        self.tick -= dt
        if self.tick <= 0:
            self.tick = self.max_tick

            if self.stone + 1 <= self.capacity:
                self.stone += 1

    def on_click(self):
        if mouse.get_pressed()[0]:
            v = [p for p in self.world.buildings_g.sprites() if
                 self.rect.colliderect(p.usage_zone) and p.name == 'storage']
            if v:
                d = self.world.max_stone - self.world.stone
                if d > self.stone:
                    d = self.stone
                self.world.stone += d
                self.stone -= d
                self.collected += d
                create_particles(GREY, self.rect.center, d, 15, self.world.particles_g)

    def draw_stats(self, dt):
        b = Rect(self.rect.x - self.rect.w / 2 - SCALE / 2, self.rect.y - 4 * SCALE + SCALE - self.stats_offset,
                 self.rect.w * 2,
                 2 * SCALE)
        sb = Surface(b.size, pygame.SRCALPHA)
        sb.fill((70, 71, 76, self.stats_alpha))
        self.world.screen.blit(sb, b.topleft)

        self.stone_w = max(self.stone_w - dt * STATS_BAR_SPEED,
                          min(self.stone_w + dt * STATS_BAR_SPEED, (self.rect.w * 2) / self.capacity * self.stone))
        f = Rect(self.rect.x - self.rect.w / 2 + SCALE / 2, self.rect.y - 4 * SCALE - self.stats_offset,
                 self.stone_w, 2 * SCALE)
        sf = Surface(f.size, pygame.SRCALPHA)
        sf.fill((224, 220, 164, self.stats_alpha))
        self.world.screen.blit(sf, f.topleft)

    def on_kill(self):
        check = [self.rect.colliderect(p.collision_rect) and
                 (p.rect.centerx == self.rect.centerx or p.rect.centery == self.rect.centery)
                 for p in self.world.pathways_g.sprites()]

        if check.count(True) < 2:
            Grass('grass', self.pos, self.world, self.world.grass_g)

            w, s = randint(1, WOOD_COST['mine'] // 2), randint(1, STONE_COST['mine'] // 2)

            wd = self.world.max_wood - self.world.wood
            if wd > w:
                wd = w
            self.world.wood += wd

            sd = self.world.max_stone - self.world.stone
            if sd > s:
                sd = s
            self.world.stone += sd
            create_particles(BLACK, self.rect.center, 10, 15, self.world.particles_g)
            self.kill()
            self.world.update_zone()


class Windmill(Tile):
    def __init__(self, pos, world, *group):
        super().__init__('windmill_1', pos, world, *group)

        self.max_tick = 60
        self.tick = self.max_tick

        self.frame = 1
        self.max_animation_tick = 30
        self.animation_tick = self.max_animation_tick

        self.frames = {
            1: self.world.images['windmill_1'],
            2: self.world.images['windmill_2']
        }

        self.zone = Rect(*self.rect.topleft,
                         self.rect.width * 5,
                         self.rect.height * 5)
        self.zone.center = self.rect.center

        self.food = 0
        self.capacity = 10

        self.world.update_zone()

        self.food_w = (self.rect.w * 2) / self.capacity * self.food

    def on_update(self, dt):
        self.tick -= dt
        if self.tick <= 0:
            self.tick = self.max_tick
            self.spread()

        self.draw_stats(dt)

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
                     self.rect.colliderect(p.collision_rect) and p.name in 'grass' and p.in_zone()]
            if tiles:
                tile = choice(tiles)
                Farmland(tile.pos, tile.world, self.world.farmland_g)
                tile.kill()

    def draw_stats(self, dt):
        b = Rect(self.rect.x - self.rect.w / 2 - SCALE / 2, self.rect.y - 4 * SCALE + SCALE - self.stats_offset,
                 self.rect.w * 2,
                 2 * SCALE)
        sb = Surface(b.size, pygame.SRCALPHA)
        sb.fill((70, 71, 76, self.stats_alpha))
        self.world.screen.blit(sb, b.topleft)

        self.food_w = max(self.food_w - dt * STATS_BAR_SPEED, min(self.food_w + dt * STATS_BAR_SPEED, (self.rect.w * 2) / self.capacity * self.food))
        f = Rect(self.rect.x - self.rect.w / 2 + SCALE / 2, self.rect.y - 4 * SCALE - self.stats_offset,
                 self.food_w, 2 * SCALE)
        sf = Surface(f.size, pygame.SRCALPHA)
        sf.fill((224, 220, 164, self.stats_alpha))
        self.world.screen.blit(sf, f.topleft)

    def on_click(self):
        if mouse.get_pressed()[0]:
            v = [p for p in self.world.buildings_g.sprites() if
                 self.rect.colliderect(p.usage_zone) and p.name == 'barn' and p.food < p.capacity]
            if v:
                barn = choice(v)
                d = barn.capacity - barn.food
                if d > self.food:
                    d = self.food
                self.food -= d
                barn.food += d
                create_particles(LIGHT_GREEN, self.rect.center, d, 15, self.world.particles_g)

    def on_kill(self):
        check = [self.rect.colliderect(p.collision_rect) and
                 (p.rect.centerx == self.rect.centerx or p.rect.centery == self.rect.centery)
                 for p in self.world.pathways_g.sprites()]

        if check.count(True) < 2:
            Grass('grass', self.pos, self.world, self.world.grass_g)

            w, s = randint(1, WOOD_COST['windmill'] // 2), randint(1, STONE_COST['windmill'] // 2)

            wd = self.world.max_wood - self.world.wood
            if wd > w:
                wd = w
            self.world.wood += wd

            sd = self.world.max_stone - self.world.stone
            if sd > s:
                sd = s
            self.world.stone += sd
            create_particles(BLACK, self.rect.center, 10, 15, self.world.particles_g)
            self.kill()
            self.world.update_zone()


class Farmland(Tile):
    def __init__(self, pos, world, *group):
        self.age = 0

        super().__init__(f'farmland_{self.age}', pos, world, *group)

        self.max_tick = randint(120, 300)
        self.tick = self.max_tick

    def grow(self):
        if randint(1, 2) == 1:
            self.age += 1
            self.name = f'farmland_{self.age}'
            self.image = self.world.images[self.name]

    def on_update(self, dt):
        if self.age < 3:
            self.tick -= 1 * dt
            if self.tick <= 0:
                if self.age == 1:
                    self.max_tick = randint(1800, 3600)
                else:
                    self.max_tick = randint(300, 600)
                self.tick = self.max_tick
                self.grow()

    def on_click(self):
        if self.age > 1:
            if self.in_zone():
                if self.age == 2:
                    v = [p for p in self.world.buildings_g.sprites() if
                         self.rect.colliderect(p.collision_rect) and 'windmill' in p.name]
                    if v:
                        windmill = choice(v)

                        d = windmill.capacity - windmill.food
                        if d > 2:
                            d = 2

                        windmill.food += d

                self.max_tick = randint(300, 600)
                self.tick = self.max_tick

                self.age = 0
                self.name = f'farmland_{self.age}'
                self.image = self.world.images[self.name]
                create_particles(BROWN, self.rect.center, 10, 15, self.world.particles_g)


    def on_kill(self):
        Grass('grass', self.pos, self.world, self.world.grass_g)

        self.kill()


class Pathway(Tile):
    def __init__(self, pos, world, *group):
        super().__init__('pathway', pos, world, *group)
        self.world.update_zone()

    def on_kill(self):
        check_1 = [self.rect.colliderect(p.collision_rect) and
                   (p.rect.centerx == self.rect.centerx or p.rect.centery == self.rect.centery)
                   and p != self
                   for p in self.world.pathways_g.sprites() + self.world.buildings_g.sprites()]

        if check_1.count(True) < 2:
            Grass('grass', self.pos, self.world, self.world.grass_g)
            create_particles(BLACK, self.rect.center, 10, 15, self.world.particles_g)
            self.kill()
            self.world.update_zone()


class Barn(Tile):
    def __init__(self, pos, world, *group):
        super().__init__('barn', pos, world, *group)

        if not self.world.house_placed:
            self.world.house_placed = True

        self.zone = Rect(*self.rect.topleft,
                         self.rect.width * 5,
                         self.rect.height * 5)
        self.zone.center = self.rect.center

        self.food = 25
        self.capacity = 50

        self.world.update_zone()
        self.food_w = (self.rect.w * 2) / self.capacity * self.food

    def draw_usage_zone(self):
        s = Surface(self.usage_zone.size, pygame.SRCALPHA)
        s.set_alpha(self.usage_zone_alpha)
        draw.rect(s, (255, 0, 0), (0, 0, *self.usage_zone.size), 1 * SCALE)
        self.world.screen.blit(s, self.usage_zone.topleft)

    def draw_stats(self, dt):
        b = Rect(self.rect.x - self.rect.w / 2 - SCALE / 2, self.rect.y - 4 * SCALE + SCALE - self.stats_offset,
                 self.rect.w * 2,
                 2 * SCALE)
        sb = Surface(b.size, pygame.SRCALPHA)
        sb.fill((70, 71, 76, self.stats_alpha))
        self.world.screen.blit(sb, b.topleft)

        self.food_w = max(self.food_w - dt * STATS_BAR_SPEED,
                          min(self.food_w + dt * STATS_BAR_SPEED, (self.rect.w * 2) / self.capacity * self.food))
        f = Rect(self.rect.x - self.rect.w / 2 + SCALE / 2, self.rect.y - 4 * SCALE - self.stats_offset,
                 self.food_w, 2 * SCALE)
        sf = Surface(f.size, pygame.SRCALPHA)
        sf.fill((224, 220, 164, self.stats_alpha))
        self.world.screen.blit(sf, f.topleft)

    def on_kill(self):
        check = [self.rect.colliderect(p.collision_rect) and
                 (p.rect.centerx == self.rect.centerx or p.rect.centery == self.rect.centery)
                 for p in self.world.pathways_g.sprites()]

        if check.count(True) < 2:
            Grass('grass', self.pos, self.world, self.world.grass_g)

            w, s = randint(1, WOOD_COST['barn'] // 2), randint(1, STONE_COST['barn'] // 2)

            wd = self.world.max_wood - self.world.wood
            if wd > w:
                wd = w
            self.world.wood += wd

            sd = self.world.max_stone - self.world.stone
            if sd > s:
                sd = s
            self.world.stone += sd
            create_particles(BLACK, self.rect.center, 10, 15, self.world.particles_g)
            self.kill()
            self.world.update_zone()

    def on_update(self, dt):
        self.draw_stats(dt)


class Storage(Tile):
    def __init__(self, pos, world, *group):
        super().__init__('storage', pos, world, *group)

        if not self.world.house_placed:
            self.world.house_placed = True

        self.zone = Rect(*self.rect.topleft,
                         self.rect.width * 5,
                         self.rect.height * 5)
        self.zone.center = self.rect.center

        self.usage_zone = Rect(*self.rect.topleft,
                               self.rect.width * 9,
                               self.rect.height * 9)
        self.usage_zone.center = self.rect.center

        self.stone_capacity = 50
        self.wood_capacity = 50

        self.world.update_zone()
        self.wood_w = (self.rect.w * 2) / self.world.max_wood * self.world.wood
        self.stone_w = (self.rect.w * 2) / self.world.max_stone * self.world.stone

    def draw_stats(self, dt):
        b1 = Rect(self.rect.x - self.rect.w / 2 - SCALE / 2, self.rect.y - 8 * SCALE + SCALE - self.stats_offset,
                 self.rect.w * 2,
                 2 * SCALE)
        sb1 = Surface(b1.size, pygame.SRCALPHA)
        sb1.fill((70, 71, 76, self.stats_alpha))
        self.world.screen.blit(sb1, b1.topleft)

        self.wood_w = max(self.wood_w - dt * STATS_BAR_SPEED,
                           min(self.wood_w + dt * STATS_BAR_SPEED,
                               (self.rect.w * 2) / self.world.max_wood * self.world.wood))
        f1 = Rect(self.rect.x - self.rect.w / 2 + SCALE / 2, self.rect.y - 8 * SCALE - self.stats_offset,
                 self.wood_w, 2 * SCALE)
        sf1 = Surface(f1.size, pygame.SRCALPHA)
        sf1.fill((224, 220, 164, self.stats_alpha))
        self.world.screen.blit(sf1, f1.topleft)

        b2 = Rect(self.rect.x - self.rect.w / 2 - SCALE / 2, self.rect.y - 4 * SCALE + SCALE - self.stats_offset,
                 self.rect.w * 2,
                 2 * SCALE)
        sb2 = Surface(b2.size, pygame.SRCALPHA)
        sb2.fill((70, 71, 76, self.stats_alpha))
        self.world.screen.blit(sb2, b2.topleft)

        self.stone_w = max(self.stone_w - dt * STATS_BAR_SPEED,
                          min(self.stone_w + dt * STATS_BAR_SPEED, (self.rect.w * 2) / self.world.max_stone * self.world.stone))
        f2 = Rect(self.rect.x - self.rect.w / 2 + SCALE / 2, self.rect.y - 4 * SCALE - self.stats_offset,
                 self.stone_w, 2 * SCALE)
        sf2 = Surface(f2.size, pygame.SRCALPHA)
        sf2.fill((224, 220, 164, self.stats_alpha))
        self.world.screen.blit(sf2, f2.topleft)

    def on_kill(self):
        check = [self.rect.colliderect(p.collision_rect) and
                 (p.rect.centerx == self.rect.centerx or p.rect.centery == self.rect.centery)
                 for p in self.world.pathways_g.sprites()]

        if check.count(True) < 2:
            Grass('grass', self.pos, self.world, self.world.grass_g)

            w, s = randint(1, WOOD_COST['storage'] // 2), randint(1, STONE_COST['storage'] // 2)

            wd = self.world.max_wood - self.world.wood
            if wd > w:
                wd = w
            self.world.wood += wd

            sd = self.world.max_stone - self.world.stone
            if sd > s:
                sd = s
            self.world.stone += sd
            create_particles(BLACK, self.rect.center, 10, 15, self.world.particles_g)
            self.kill()
            self.world.update_zone()

    def draw_usage_zone(self):
        s = Surface(self.usage_zone.size, pygame.SRCALPHA)
        s.set_alpha(self.usage_zone_alpha)
        draw.rect(s, (0, 0, 255), (0, 0, *self.usage_zone.size), 1 * SCALE)
        self.world.screen.blit(s, self.usage_zone.topleft)
