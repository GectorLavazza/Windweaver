import pygame

FPS = 30

pygame.display.init()
screen_info = pygame.display.Info()


def fit_aspect_ratio(screen_width, screen_height,
                     target_width=320, target_height=180):
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


w, h = 320 * 6, 180 * 6
# w, h = screen_info.current_w, screen_info.current_h
screen_width, screen_height = fit_aspect_ratio(w, h)

WIDTH, HEIGHT = 320, 180

SCALE = screen_width / WIDTH
CENTER = pygame.Vector2(screen_width // 2, screen_height // 2)

TILE_SIZE = 8
MAP_WIDTH, MAP_HEIGHT = 128, 128

MAX_ZOOM = 2
MIN_ZOOM = 0.5
