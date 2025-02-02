FPS = 30

SCALE = 4
TILE_SIZE = 8 * SCALE
MAP_WIDTH, MAP_HEIGHT = 48, 38  # 48 x 48

WIDTH, HEIGHT = 320 * SCALE, 180 * SCALE

screen_width, screen_height = WIDTH, HEIGHT
screen_size = screen_width, screen_height

CENTER = screen_width // 2, screen_height // 2

MAP_SIZE = TILE_SIZE * MAP_WIDTH, TILE_SIZE * MAP_HEIGHT

GROWTH_MIN = 3600
GROWTH_MAX = 36000

WOOD_COST = {'house': 5,
             'mine': 5,
             'windmill': 10,
             'pathway': 1,
             'barn': 10,
             'storage': 15}
STONE_COST = {'house': 5,
             'mine': 10,
             'windmill': 5,
              'pathway': 1,
              'barn': 10,
              'storage': 15}

DAY_TIME = 4500

MODES = ['house', 'pathway', 'windmill', 'barn', 'mine', 'storage']

STATS_ALPHA_SPEED = 40
STATS_OFFSET_SPEED = 3
OUTLINE_ALPHA_SPEED = 7
STATS_BAR_SPEED = 2

GREEN = '#508714'
BLACK = '#26171b'
WHITE = '#508714'
LIGHT_GREEN = '#b5bd3d'
GREY = '#7a7070'
ORANGE = '#c0552a'
BROWN = '#6d3e0f'
