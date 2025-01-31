FPS = 120

TILE_SIZE = 8
MAP_WIDTH, MAP_HEIGHT = 64, 64  # 48 x 48

WIDTH, HEIGHT = 320, 180

screen_width, screen_height = WIDTH, HEIGHT
screen_size = screen_width, screen_height

CENTER = screen_width // 2, screen_height // 2

MAP_SIZE = TILE_SIZE * MAP_WIDTH, TILE_SIZE * MAP_HEIGHT

GROWTH_MIN = 3600
GROWTH_MAX = 36000

WOOD_COST = {'house': 5,
             'mine': 5,
             'windmill': 10,
             'pathway': 1}
STONE_COST = {'house': 5,
             'mine': 10,
             'windmill': 5,
              'pathway': 1}

DAY_TIME = 9000
