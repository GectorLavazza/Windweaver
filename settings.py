from random import randint

FPS = 60

WIDTH, HEIGHT = 320, 180

screen_width, screen_height = WIDTH, HEIGHT
screen_size = screen_width, screen_height

CENTER = screen_width // 2, screen_height // 2

TILE_SIZE = 8

CHUNK_WIDTH, CHUNK_HEIGHT = 32, 32
CHUNK_SIZE = TILE_SIZE * CHUNK_WIDTH, TILE_SIZE * CHUNK_HEIGHT

GROWTH_MIN = 3600
GROWTH_MAX = 36000

WOOD_COST = {'house': 0,
             'mine': 0,
             'windmill': 0}
STONE_COST = {'house': 0,
              'mine': 0,
              'windmill': 0}

DAY_TIME = 9000

SCALE = 30.0
OCTAVES = 5
PERSISTENCE = 0.55
LACUNARITY = 5
SEED = randint(0, 10000)

print('-' * 20)
print(f'Seed: {SEED}')

COLORS = {
    'water': (0, 0, 255),
    'grass': (0, 255, 0),
    'forest': (0, 128, 0),
    'mountains': (128, 128, 128),
    'snow': (255, 255, 255)
}
