import pygame

COLOR = (91, 155, 69)
obstacle_sprites_group = pygame.sprite.Group()
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, info_rect, group):
        super().__init__(group)

        x, y, width, height = info_rect

        self.image = pygame.Surface((width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.mask = pygame.mask.from_surface(self.image)

class World:
    def create_rect(self):
        info_rects = [
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

        for info_rect in info_rects:
            Obstacle(info_rect, obstacle_sprites_group)

    def draw_rects(self, win):
        for sprite in obstacle_sprites_group:
            pygame.draw.rect(win, COLOR, sprite.rect)