import pygame

FPS = 30

pygame.display.init()
screen_info = pygame.display.Info()


def fit_aspect_ratio(screen_width, screen_height,
                     target_width=320, target_height=180):
    # Calculate the aspect ratio
    aspect_ratio = target_width / target_height

    # Calculate the maximum width and height that fit within the screen dimensions
    max_width = screen_width
    max_height = screen_height

    # Calculate the height based on the max width
    height_based_on_width = max_width / aspect_ratio
    if height_based_on_width <= max_height:
        return int(max_width), int(height_based_on_width)

    # Calculate the width based on the max height
    width_based_on_height = max_height * aspect_ratio
    if width_based_on_height <= max_width:
        return int(width_based_on_height), int(max_height)

    # If neither fits, return the largest fitting size
    return int(max_width), int(max_height)

# screen_width, screen_height = 320 * 6, 180 * 6
w, h = screen_info.current_w, screen_info.current_h
screen_width, screen_height = fit_aspect_ratio(w, h)

WIDTH, HEIGHT = 320, 180

SCALE = screen_width / WIDTH
CENTER = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

TILE_SIZE = 8
MAP_WIDTH, MAP_HEIGHT = 64, 64

