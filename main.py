import random
import time

from cursor import Cursor
from map import Map
from settings import *


def main():
    pygame.init()
    pygame.mouse.set_visible(False)

    screen = pygame.display.set_mode((screen_width, screen_height),
                                     pygame.DOUBLEBUF | pygame.SRCALPHA)
    screen_rect = screen.get_rect()
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    seed = random.randint(0, 100)
    map = Map(surface, seed, CENTER)

    cursor_g = pygame.sprite.Group()

    cursor = Cursor(cursor_g)

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

            if event == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        map.update(dt)

        screen.blit(pygame.transform.scale_by(surface, SCALE), (0, 0))

        cursor_g.draw(screen)
        cursor.update()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
