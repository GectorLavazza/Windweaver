import pygame

FPS = 60

pygame.display.init()
screen_info = pygame.display.Info()

WIDTH, HEIGHT = 320, 180


def fit_aspect_ratio(screen_width, screen_height,
                     target_width=WIDTH, target_height=HEIGHT):
    aspect_ratio = target_width / target_height

    max_width = screen_width
    max_height = screen_height

    height_based_on_width = max_width / aspect_ratio
    if height_based_on_width <= max_height:
        return int(max_width), int(height_based_on_width)

    width_based_on_height = max_height * aspect_ratio
    if width_based_on_height <= max_width:
        return int(width_based_on_height), int(max_height)

    return int(max_width), int(max_height)


w, h = 320 * 3, 180 * 3
# w, h = screen_info.current_w, screen_info.current_h
screen_width, screen_height = fit_aspect_ratio(w, h)
screen_size = screen_width, screen_height

SCALE = screen_width / WIDTH
CENTER = pygame.Vector2(screen_width // 2, screen_height // 2)

TILE_SIZE = 8
MAP_WIDTH, MAP_HEIGHT = 64, 64
MAP_SIZE = TILE_SIZE * MAP_WIDTH * SCALE, TILE_SIZE * MAP_HEIGHT * SCALE
