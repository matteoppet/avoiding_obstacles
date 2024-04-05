import pygame

COLOR = (110, 128, 113)
obstacle_sprites_group = pygame.sprite.Group()
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, info_rect, group):
        super().__init__(group)

        x, y, width, height = info_rect

        self.image = pygame.Surface((width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.mask = pygame.mask.from_surface(self.image)

class World:
    def create_rect(self, window_size):
        info_rects = self.bounds_window(window_size)

        for info_rect in info_rects:
            Obstacle(info_rect, obstacle_sprites_group)

    def bounds_window(self, window_size):
        x_window = window_size[0]
        y_window = window_size[1]

        return [
            (-50, 0, 50, y_window),
            (0, -50, x_window, 50),
            (x_window, 0, x_window+50, y_window),
            (0, y_window, x_window, y_window+50)
        ]
    
    def rect_in_map(self):
        return [
            (0, 0, 500, 150), 
            (650, 0, 800, 150), 
            (0, 250, 900, 150), 
            (1000, 250, 400, 150), 
            (0, 500, 650, 250), 
            (800, 500, 700, 250),
            (500, 0, 150, 20),
            (0, 150, 20, 100),
            (1260, 150, 20, 100),
            (0, 400, 20, 100),
            (1260, 400, 20, 100),
            (650, 700, 200, 20)
        ]

    def draw_rects(self, win):
        for sprite in obstacle_sprites_group:
            pygame.draw.rect(win, COLOR, sprite.rect)