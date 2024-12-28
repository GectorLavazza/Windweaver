import pygame

FPS = 30

WIDTH, HEIGHT = 320, 180
screen_width, screen_height = 320 * 6, 180 * 6  # 1920x1080
SCALE = screen_width // WIDTH
CENTER = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

TILE_SIZE = 8
MAP_WIDTH, MAP_HEIGHT = 64, 64
