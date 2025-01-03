from pygame import Vector2, mouse, Surface, Rect

from chunk import Chunk
from engine import Engine
from settings import screen_width, screen_height, CHUNK_WIDTH, CHUNK_HEIGHT, \
    TILE_SIZE


class World:
    def __init__(self, screen: Surface, center, sky, engine: Engine):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.engine = engine
        self.surface = Surface((screen_width, screen_height))  # Fixed size
        self.rect = self.surface.get_rect()
        self.rect.center = center

        self.speed = 3
        self.edge_threshold = screen_height // 4

        self.dx = 0
        self.dy = 0
        self.dynamic_speed_x = 0
        self.dynamic_speed_y = 0
        self.velocity = Vector2(0, 0)

        self.sky = sky
        self.camera_offset = Vector2(0, 0)

        self.chunks = {}

        self.visible_rect = self.screen_rect
        self.visible_rect = self.visible_rect.clip(self.surface.get_rect())

    def update(self, dt):
        if self.check_mouse_edges():
            self.move(dt)

        self.update_chunks()
        self.draw_chunks()

    def draw_chunks(self):
        for chunk_pos, chunk in self.chunks.items():
            screen_chunk_pos = (
                chunk.pos[0] * CHUNK_WIDTH * TILE_SIZE - self.camera_offset.x,
                chunk.pos[1] * CHUNK_HEIGHT * TILE_SIZE - self.camera_offset.y,
            )
            self.surface.blit(chunk.surface, screen_chunk_pos)

        self.screen.blit(self.surface, (0, 0), self.visible_rect)

    def update_chunks(self):
        visible_chunks = self.get_visible_chunks()

        for chunk_pos in visible_chunks:
            if chunk_pos not in self.chunks:
                self.chunks[chunk_pos] = Chunk(chunk_pos, self.engine)

    def get_visible_chunks(self):
        start_x = int(self.camera_offset.x // (CHUNK_WIDTH * TILE_SIZE))
        start_y = int(self.camera_offset.y // (CHUNK_HEIGHT * TILE_SIZE))
        end_x = int(
            (self.camera_offset.x + screen_width) // (CHUNK_WIDTH * TILE_SIZE))
        end_y = int((self.camera_offset.y + screen_height) // (
                    CHUNK_HEIGHT * TILE_SIZE))

        visible_chunks = [
            (x, y)
            for x in range(start_x, end_x + 1)
            for y in range(start_y, end_y + 1)
        ]

        return visible_chunks

    def check_mouse_edges(self):
        mouse_x, mouse_y = mouse.get_pos()

        self.dx = 0
        self.dy = 0

        if mouse_x < self.edge_threshold:
            self.dx = -1
            distance_to_edge = self.edge_threshold - mouse_x
            self.dynamic_speed_x = distance_to_edge / self.edge_threshold

        elif mouse_x > screen_width - self.edge_threshold:
            self.dx = 1
            distance_to_edge = mouse_x - (screen_width - self.edge_threshold)
            self.dynamic_speed_x = distance_to_edge / self.edge_threshold

        if mouse_y < self.edge_threshold:
            self.dy = -1
            distance_to_edge = self.edge_threshold - mouse_y
            self.dynamic_speed_y = distance_to_edge / self.edge_threshold

        elif mouse_y > screen_height - self.edge_threshold:
            self.dy = 1
            distance_to_edge = mouse_y - (screen_height - self.edge_threshold)
            self.dynamic_speed_y = distance_to_edge / self.edge_threshold

        return self.dx != 0 or self.dy != 0

    def move(self, dt):
        input_direction = Vector2(self.dx, self.dy)
        if input_direction.length() > 0:
            input_direction = input_direction.normalize()

        speed_multiplier_x = max(0, min(1, self.dynamic_speed_x))
        speed_multiplier_y = max(0, min(1, self.dynamic_speed_y))

        self.velocity.x = input_direction.x * self.speed * speed_multiplier_x * dt
        self.velocity.y = input_direction.y * self.speed * speed_multiplier_y * dt

        self.camera_offset += self.velocity

        self.visible_rect.topleft = -Vector2(self.rect.topleft)
