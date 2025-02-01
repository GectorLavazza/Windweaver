FPS = 30

SCALE = 4
TILE_SIZE = 8 * SCALE
MAP_WIDTH, MAP_HEIGHT = 48, 48  # 48 x 48

WIDTH, HEIGHT = 320 * SCALE, 180 * SCALE

screen_width, screen_height = WIDTH, HEIGHT
screen_size = screen_width, screen_height

CENTER = screen_width // 2, screen_height // 2

MAP_SIZE = TILE_SIZE * MAP_WIDTH, TILE_SIZE * MAP_HEIGHT

GROWTH_MIN = 3600
GROWTH_MAX = 36000

# WOOD_COST = {'house': 5,
#              'mine': 5,
#              'windmill': 10,
#              'pathway': 1,
#              'barn': 10,
#              'storage': 20}
# STONE_COST = {'house': 5,
#              'mine': 10,
#              'windmill': 5,
#               'pathway': 1,
#               'barn': 10,
#               'storage': 20}

WOOD_COST = {'house': 0,
             'mine': 0,
             'windmill': 0,
             'pathway': 0,
             'barn': 0,
             'storage': 0}
STONE_COST = {'house': 0,
             'mine': 0,
             'windmill': 0,
              'pathway': 0,
              'barn': 0,
              'storage': 0}

DAY_TIME = 9000
