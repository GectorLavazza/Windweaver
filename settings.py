FPS = 120

WIDTH, HEIGHT = 320, 180
screen_width, screen_height = WIDTH * 4, HEIGHT * 4
SCALE = screen_width // WIDTH
screen_size = screen_width, screen_height

CENTER = screen_width // 2, screen_height // 2

TILE_SIZE = 8 * SCALE
MAP_WIDTH, MAP_HEIGHT = 64, 64  # 48 x 48

MAP_SIZE = TILE_SIZE * MAP_WIDTH, TILE_SIZE * MAP_HEIGHT

GROWTH_MIN = 3600
GROWTH_MAX = 36000

WOOD_COST = {'house': 0,
             'mine': 0,
             'windmill': 0}
STONE_COST = {'house': 0,
             'mine': 0,
             'windmill': 0}

DAY_TIME = 9000
