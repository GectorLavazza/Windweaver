FPS = 120

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


# w, h = WIDTH * 3, HEIGHT * 3
# w, h = screen_info.current_w, screen_info.current_h
# screen_width, screen_height = fit_aspect_ratio(w, h)
screen_width, screen_height = WIDTH, HEIGHT
screen_size = screen_width, screen_height

# SCALE = screen_width / WIDTH
SCALE = 1
CENTER = screen_width // 2, screen_height // 2

TILE_SIZE = 8
MAP_WIDTH, MAP_HEIGHT = 128, 128  # 48 x 48
MAP_SIZE = TILE_SIZE * MAP_WIDTH * SCALE, TILE_SIZE * MAP_HEIGHT * SCALE

GROWTH_MIN = 3600
GROWTH_MAX = 36000

WOOD_COST = {'house': 0,
             'mine': 0,
             'windmill': 0}
STONE_COST = {'house': 0,
             'mine': 0,
             'windmill': 0}

DAY_TIME = 9000
