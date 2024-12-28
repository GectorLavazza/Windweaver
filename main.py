import random
import time


from map import Map
from settings import *

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)
screen_rect = screen.get_rect()

surface = pygame.Surface((WIDTH, HEIGHT))

seed = random.randint(0, 100)
map = Map(surface, seed, CENTER)

running = True
clock = pygame.time.Clock()

last_time = time.time()

while running:
    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:  # Move up
                map.dy = 1
            if event.key == pygame.K_s:  # Move down
                map.dy = -1
            if event.key == pygame.K_a:  # Move left
                map.dx = 1
            if event.key == pygame.K_d:  # Move right
                map.dx = -1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:  # Move up
                map.dy = 0
            if event.key == pygame.K_s:  # Move down
                map.dy = 0
            if event.key == pygame.K_a:  # Move left
                map.dx = 0
            if event.key == pygame.K_d:  # Move right
                map.dx = 0

    map.update(dt)

    pygame.display.flip()

    screen.blit(pygame.transform.scale_by(surface, SCALE), (0, 0))

    clock.tick(FPS)

pygame.quit()
