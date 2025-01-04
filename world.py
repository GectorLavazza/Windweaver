from pygame import Vector2, mouse, Surface, Rect

from chunk import Chunk
from engine import Engine
from settings import screen_width, screen_height, CHUNK_WIDTH, CHUNK_HEIGHT, \
    TILE_SIZE, screen_size


class World:
    def __init__(self, screen: Surface, center, sky, engine: Engine):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.engine = engine
        self.surface = Surface(screen_size)  # Fixed size
        self.rect = self.surface.get_rect()
        self.rect.center = center

        self.speed = 10
        self.edge_threshold = screen_height // 4

        self.d = Vector2(0, 0)
        self.dynamic_speed = Vector2(0, 0)
        self.velocity = Vector2(0, 0)

        self.sky = sky
        self.camera_pos = Vector2(0, 0)

        self.chunks = {}

        self.visible_rect = self.screen_rect
        self.visible_rect = self.visible_rect.clip(self.surface.get_rect())

    def update(self, dt):
        if self.check_mouse_edges():
            self.move(dt)

        self.update_chunks()
        self.draw_chunks(dt)

    def draw_chunks(self, dt):
        for pos, chunk in self.chunks.items():
            chunk.update(dt)

    def draw(self):
        self.screen.blit(self.surface, (0, 0), self.visible_rect)

    def update_chunks(self):
        visible_chunks = self.get_visible_chunks()

        for chunk_pos in visible_chunks:
            if chunk_pos not in self.chunks:
                self.chunks[chunk_pos] = Chunk(chunk_pos, self, self.engine)

    def get_visible_chunks(self):
        start_x = int(self.camera_pos.x // (CHUNK_WIDTH * TILE_SIZE))
        start_y = int(self.camera_pos.y // (CHUNK_HEIGHT * TILE_SIZE))
        end_x = int(
            (self.camera_pos.x + screen_width) // (CHUNK_WIDTH * TILE_SIZE))
        end_y = int((self.camera_pos.y + screen_height) // (
                CHUNK_HEIGHT * TILE_SIZE))

        visible_chunks = [
            (x, y)
            for x in range(start_x, end_x + 1)
            for y in range(start_y, end_y + 1)
        ]

        return visible_chunks

    def check_mouse_edges(self):
        mouse_pos = Vector2(mouse.get_pos())

        self.d = Vector2(0, 0)

        if mouse_pos.x < self.edge_threshold:
            self.d.x = -1
            distance_to_edge = self.edge_threshold - mouse_pos.x
            self.dynamic_speed.x = distance_to_edge / self.edge_threshold

        elif mouse_pos.x > screen_width - self.edge_threshold:
            self.d.x = 1
            distance_to_edge = mouse_pos.x - (
                        screen_width - self.edge_threshold)
            self.dynamic_speed.x = distance_to_edge / self.edge_threshold

        if mouse_pos.y < self.edge_threshold:
            self.d.y = -1
            distance_to_edge = self.edge_threshold - mouse_pos.y
            self.dynamic_speed.y = distance_to_edge / self.edge_threshold

        elif mouse_pos.y > screen_height - self.edge_threshold:
            self.d.y = 1
            distance_to_edge = mouse_pos.y - (
                        screen_height - self.edge_threshold)
            self.dynamic_speed.y = distance_to_edge / self.edge_threshold

        return self.d.x or self.d.y

    def move(self, dt):
        input_direction = Vector2(self.d.x, self.d.y)
        if input_direction.length() > 0:
            input_direction = input_direction.normalize()

        speed_multiplier = Vector2(max(0, min(1, self.dynamic_speed.x)),
                                   max(0, min(1, self.dynamic_speed.y)))

        self.velocity.x = input_direction.x * self.speed * speed_multiplier.x * dt
        self.velocity.y = input_direction.y * self.speed * speed_multiplier.y * dt

        self.camera_pos += self.velocity

        self.visible_rect.topleft = -Vector2(self.rect.topleft)
